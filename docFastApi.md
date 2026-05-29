# Guia de Integração — Next.js com TaskInsight Analytics API

Este documento descreve como o frontend Next.js deve consumir a API de métricas do TaskInsight, incluindo autenticação, comportamento por role e exemplos práticos de implementação.

---

## Visão Geral

A API de analytics **não realiza login nem gerencia usuários**. Ela apenas valida o token JWT gerado pela API de CRUD e usa as informações do payload para filtrar os dados retornados.

```
[Next.js] → login → [API de CRUD] → retorna JWT
[Next.js] → requisição com JWT → [API de Analytics] → retorna métricas
```

---

## Variáveis de Ambiente

No projeto Next.js, crie o arquivo `.env.local`:

```env
NEXT_PUBLIC_ANALYTICS_API_URL=http://127.0.0.1:8000
```

> Em produção, substitua pela URL real da API de analytics.

---

## Como o Token é Validado

O token JWT deve ser gerado pela API de CRUD com o seguinte payload:

```json
{
  "userId": "6a146b2ce695ae2b77e1e8d3",
  "role": "user",
  "iat": 1779824359,
  "exp": 1779827959
}
```

A API de analytics extrai `userId` e `role` do token e usa essas informações para filtrar os dados. O token deve ser enviado em todas as requisições no header:

```
Authorization: Bearer <token>
```

### Erros de autenticação

| Código | Motivo |
|--------|--------|
| `401`  | Token não fornecido |
| `401`  | Token expirado |
| `401`  | Token inválido ou campos `userId`/`role` ausentes |
| `500`  | Configuração interna da API com problema |

---

## Comportamento por Role

Este é o ponto mais importante da integração. O mesmo endpoint retorna dados diferentes dependendo do `role` contido no token.

### `role: user`
- Retorna métricas **apenas das tarefas do usuário autenticado**
- O filtro `userId` é aplicado automaticamente na query do MongoDB
- O frontend **não precisa enviar o userId** — ele é extraído do token

### `role: admin`
- Retorna métricas **de todos os usuários**
- Nenhum filtro de `userId` é aplicado
- Ideal para dashboards administrativos com visão global

```
Mesmo endpoint → mesmo token → role diferente → dados diferentes
```

---

## Rotas Disponíveis

### `GET /task/metrics/by-status`

Retorna distribuição de tarefas por status.

**Comportamento:**
- `role: user` → conta apenas as tarefas do usuário autenticado
- `role: admin` → conta todas as tarefas do sistema

**Response:**
```json
{
  "success": true,
  "data": {
    "total_tasks": 4,
    "PENDING":     { "count": 2, "percent": 50.0 },
    "IN_PROGRESS": { "count": 0, "percent": 0.0  },
    "DONE":        { "count": 2, "percent": 50.0 },
    "CANCELLED":   { "count": 0, "percent": 0.0  }
  }
}
```

---

### `GET /task/metrics/by-priority`

Retorna distribuição de tarefas por prioridade.

**Comportamento:**
- `role: user` → conta apenas as tarefas do usuário autenticado
- `role: admin` → conta todas as tarefas do sistema

**Response:**
```json
{
  "success": true,
  "data": {
    "total_tasks": 4,
    "HIGH":   { "count": 2, "percent": 50.0 },
    "MEDIUM": { "count": 1, "percent": 25.0 },
    "LOW":    { "count": 1, "percent": 25.0 }
  }
}
```

---

### `GET /task/metrics/average-time`

Retorna o tempo médio para conclusão de tarefas.

**Comportamento:**
- Considera apenas tarefas com `status: DONE`, `completedAt` e `startedAt` preenchidos
- Retorna `0` se não houver tarefas concluídas com `startedAt` preenchido
- `role: user` → média apenas das tarefas do usuário autenticado
- `role: admin` → média de todas as tarefas do sistema

> **Atenção:** A API de CRUD deve garantir que `startedAt` seja preenchido ao mover uma tarefa para `IN_PROGRESS`. Sem isso, esta métrica retornará `0`.

**Response:**
```json
{
  "success": true,
  "data": {
    "average_time_seconds": 5205.27,
    "average_time_hours":   1.45,
    "average_time_days":    0.06
  }
}
```

---

## Implementação no Next.js

### Tipagens — `types/metrics.ts`

```ts
export interface StatusItem {
  count: number;
  percent: number;
}

export interface MetricsByStatusResponse {
  success: boolean;
  data: {
    total_tasks: number;
    PENDING: StatusItem;
    IN_PROGRESS: StatusItem;
    DONE: StatusItem;
    CANCELLED: StatusItem;
  };
}

export interface MetricsByPriorityResponse {
  success: boolean;
  data: {
    total_tasks: number;
    HIGH: StatusItem;
    MEDIUM: StatusItem;
    LOW: StatusItem;
  };
}

export interface AverageTimeResponse {
  success: boolean;
  data: {
    average_time_seconds: number;
    average_time_hours: number;
    average_time_days: number;
  };
}
```

---

### Utilitário de requisição — `lib/analyticsApi.ts`

```ts
const BASE_URL = process.env.NEXT_PUBLIC_ANALYTICS_API_URL;

async function fetchMetrics<T>(endpoint: string, token: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    cache: 'no-store',
  });

  if (res.status === 401) throw new Error('Token expirado ou inválido');
  if (!res.ok) throw new Error(`Erro ao buscar ${endpoint}: ${res.status}`);

  return res.json();
}

export const analyticsApi = {
  getByStatus:   (token: string) => fetchMetrics<MetricsByStatusResponse>('/task/metrics/by-status', token),
  getByPriority: (token: string) => fetchMetrics<MetricsByPriorityResponse>('/task/metrics/by-priority', token),
  getAverageTime:(token: string) => fetchMetrics<AverageTimeResponse>('/task/metrics/average-time', token),
};
```

---

### Onde armazenar o token

O token deve ser armazenado em cookie `httpOnly` pela API de CRUD no momento do login. Isso impede acesso via JavaScript e é mais seguro que `localStorage`.

```ts
// API de CRUD — ao fazer login, define o cookie
res.cookie('token', jwtToken, {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  sameSite: 'strict',
  maxAge: 60 * 60 * 1000, // 1 hora
});
```

No Next.js, leia o cookie nos Server Components:

```ts
import { cookies } from 'next/headers';

const token = cookies().get('token')?.value ?? '';
```

---

### Dashboard — Server Component — `app/dashboard/page.tsx`

```tsx
import { analyticsApi } from '@/lib/analyticsApi';
import { cookies } from 'next/headers';

export default async function DashboardPage() {
  const token = cookies().get('token')?.value ?? '';

  const [statusData, priorityData, avgTimeData] = await Promise.all([
    analyticsApi.getByStatus(token),
    analyticsApi.getByPriority(token),
    analyticsApi.getAverageTime(token),
  ]);

  return (
    <div>
      <h1>Dashboard</h1>

      <section>
        <h2>Por Status</h2>
        <p>Total: {statusData.data.total_tasks}</p>
        <p>Pendentes: {statusData.data.PENDING.count} ({statusData.data.PENDING.percent}%)</p>
        <p>Em andamento: {statusData.data.IN_PROGRESS.count} ({statusData.data.IN_PROGRESS.percent}%)</p>
        <p>Concluídas: {statusData.data.DONE.count} ({statusData.data.DONE.percent}%)</p>
        <p>Canceladas: {statusData.data.CANCELLED.count} ({statusData.data.CANCELLED.percent}%)</p>
      </section>

      <section>
        <h2>Por Prioridade</h2>
        <p>Alta: {priorityData.data.HIGH.count} ({priorityData.data.HIGH.percent}%)</p>
        <p>Média: {priorityData.data.MEDIUM.count} ({priorityData.data.MEDIUM.percent}%)</p>
        <p>Baixa: {priorityData.data.LOW.count} ({priorityData.data.LOW.percent}%)</p>
      </section>

      <section>
        <h2>Tempo Médio de Conclusão</h2>
        <p>{avgTimeData.data.average_time_hours}h ({avgTimeData.data.average_time_days} dias)</p>
      </section>
    </div>
  );
}
```

---

### Dashboard Admin — exibindo dados de todos os usuários

Quando o token contém `role: admin`, a API retorna automaticamente os dados globais. No frontend, você pode exibir uma indicação visual:

```tsx
import { cookies } from 'next/headers';
import { jwtDecode } from 'jwt-decode';

export default async function DashboardPage() {
  const token = cookies().get('token')?.value ?? '';
  const payload = jwtDecode<{ role: string }>(token);
  const isAdmin = payload.role === 'admin';

  const statusData = await analyticsApi.getByStatus(token);

  return (
    <div>
      {isAdmin && <p>Visão global — todos os usuários</p>}
      <p>Total de tarefas: {statusData.data.total_tasks}</p>
    </div>
  );
}
```

> Instale o pacote: `npm install jwt-decode`

---

### Client Component com SWR — `components/MetricsByStatus.tsx`

```tsx
'use client';

import useSWR from 'swr';
import { MetricsByStatusResponse } from '@/types/metrics';

const fetcher = ([url, token]: [string, string]) =>
  fetch(url, { headers: { Authorization: `Bearer ${token}` } }).then(r => {
    if (!r.ok) throw new Error('Erro na requisição');
    return r.json();
  });

export default function MetricsByStatus({ token }: { token: string }) {
  const { data, error, isLoading } = useSWR<MetricsByStatusResponse>(
    [`${process.env.NEXT_PUBLIC_ANALYTICS_API_URL}/task/metrics/by-status`, token],
    fetcher,
    { refreshInterval: 30000 } // atualiza a cada 30 segundos
  );

  if (isLoading) return <p>Carregando...</p>;
  if (error) return <p>Erro ao carregar métricas.</p>;

  return (
    <div>
      <p>Total: {data?.data.total_tasks}</p>
      <p>Concluídas: {data?.data.DONE.count} ({data?.data.DONE.percent}%)</p>
    </div>
  );
}
```

---

### Proteção de rotas — `middleware.ts`

Redireciona para login caso o token não esteja presente:

```ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  if (!token) return NextResponse.redirect(new URL('/login', request.url));
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

---

### Tratamento de token expirado

Quando a API retorna `401`, o frontend deve redirecionar para o login e limpar o cookie:

```ts
// lib/analyticsApi.ts
if (res.status === 401) {
  // Em Client Components:
  document.cookie = 'token=; Max-Age=0; path=/';
  window.location.href = '/login';
  throw new Error('Sessão expirada');
}
```

Em Server Components, use `redirect` do Next.js:

```ts
import { redirect } from 'next/navigation';

try {
  const data = await analyticsApi.getByStatus(token);
} catch (e) {
  redirect('/login');
}
```

---

## Resumo do Fluxo Completo

```
1. Usuário faz login na API de CRUD
2. API de CRUD retorna JWT com { userId, role }
3. Next.js armazena o JWT em cookie httpOnly
4. Next.js envia o JWT no header Authorization para a API de analytics
5. API de analytics valida o JWT e extrai userId e role
6. Se role = user  → filtra tarefas pelo userId
7. Se role = admin → retorna dados de todos os usuários
8. Next.js exibe as métricas no dashboard
```

---

## Checklist de Integração

- [ ] `.env.local` com `NEXT_PUBLIC_ANALYTICS_API_URL` configurado
- [ ] Token armazenado em cookie `httpOnly`
- [ ] Header `Authorization: Bearer <token>` enviado em todas as requisições
- [ ] Tratamento de erro `401` com redirecionamento para login
- [ ] `middleware.ts` protegendo as rotas do dashboard
- [ ] `cache: 'no-store'` nas requisições para garantir dados atualizados
- [ ] Tipagens TypeScript criadas em `types/metrics.ts`
