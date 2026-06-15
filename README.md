# taskinsight-data-analysis

API de análise de dados e métricas do TaskInsight, responsável por processar e expor métricas das tarefas armazenadas no MongoDB.

> Esta API é responsável **apenas por métricas e análise de dados**. O CRUD das tarefas é gerenciado por uma API separada.

---

## Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [Motor](https://motor.readthedocs.io/) (MongoDB async)
- [Python 3.11+](https://www.python.org/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)
- [MongoDB Atlas](https://www.mongodb.com/atlas)

---

## Pré-requisitos

- Python 3.11+
- MongoDB
- pip

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/taskinsight-squad-2/taskinsight-data-analysis.git
cd taskinsight-data-analysis

# Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
MONGODB_URL=mongodb+srv://<user>:<password>@cluster0.mongodb.net/?appName=Cluster0
SECRET_KEY=sua_chave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> O `SECRET_KEY` deve ser **idêntico** ao `JWT_SECRET` configurado na API de CRUD para que os tokens sejam validados corretamente.

---

## Executando

```bash
fastapi dev main.py
```

- API disponível em: `http://127.0.0.1:8000`
- Documentação Swagger em: `http://127.0.0.1:8000/docs`

---

## Autenticação

Todas as rotas são protegidas por JWT Bearer Token. O token é gerado pela API de CRUD no momento do login e deve ser enviado no header de todas as requisições:

```
Authorization: Bearer <token>
```

O payload do token deve conter:

```json
{
  "userId": "string",
  "role": "user | admin"
}
```

- `role: user` — retorna métricas apenas do usuário autenticado
- `role: admin` — retorna métricas de todos os usuários

---

## Rotas

### GET `/task/metrics/by-status`

Retorna a quantidade e percentual de tarefas agrupadas por status.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_tasks": 4,
    "PENDING": { "count": 2, "percent": 50.0 },
    "IN_PROGRESS": { "count": 0, "percent": 0.0 },
    "DONE": { "count": 2, "percent": 50.0 },
    "CANCELLED": { "count": 0, "percent": 0.0 }
  }
}
```

---

### GET `/task/metrics/by-priority`

Retorna a quantidade e percentual de tarefas agrupadas por prioridade.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_tasks": 4,
    "HIGH": { "count": 2, "percent": 50.0 },
    "MEDIUM": { "count": 1, "percent": 25.0 },
    "LOW": { "count": 1, "percent": 25.0 }
  }
}
```

---

### GET `/task/metrics/average-time`

Retorna o tempo médio para conclusão de tarefas com status `DONE` que possuem `startedAt` preenchido.

> Retorna `0` para tarefas concluídas sem `startedAt` preenchido. A validação de `startedAt` obrigatório deve ser garantida pela API de CRUD.

**Response:**
```json
{
  "success": true,
  "data": {
    "average_time_seconds": 5205.27,
    "average_time_hours": 1.45,
    "average_time_days": 0.06
  }
}
```

---

### GET `/task/metrics/throughput`

Retorna a quantidade de tarefas concluídas agrupadas por dia, ordenadas por data.

**Response:**
```json
{
  "success": true,
  "data": [
    { "day": "2026-05-25", "count": 3 },
    { "day": "2026-05-26", "count": 2 }
  ]
}
```

---

### GET `/task/metrics/backlog`

Retorna a diferença entre tarefas criadas e finalizadas por dia, calculada com pandas.

> Considera apenas tarefas finalizadas (`DONE`) no mesmo dia em que foram criadas para o cálculo de `finalizadas`.

**Response:**
```json
{
  "success": true,
  "data": [
    { "date": "2026-05-25", "criadas": 3, "finalizadas": 1, "backlog": 2 },
    { "date": "2026-05-26", "criadas": 2, "finalizadas": 2, "backlog": 0 }
  ]
}
```

---

### GET `/task/metrics/response-time`

Retorna o percentual de tarefas atendidas dentro do SLA (até 3 horas) agrupadas por dia.

- Se `startedAt` estiver preenchido, calcula o tempo entre `createdAt` e `startedAt`
- Se `startedAt` for `null`, usa o tempo atual como referência
- SLA considerado cumprido quando o tempo de resposta é ≤ 3 horas
- `target` fixo de 90% indica a meta de SLA esperada

**Response:**
```json
{
  "success": true,
  "data": [
    { "date": "2026-05-25", "slaPercentage": 85.0, "target": 90 },
    { "date": "2026-05-26", "slaPercentage": 100.0, "target": 90 }
  ]
}
```

---

## Estrutura do Projeto

```
├── middlewares/
│   └── auth.py                          # Validação JWT
├── pipelines/
│   ├── tasks_by_status_pipeline.py
│   ├── tasks_by_priority_pipeline.py
│   ├── task_average_time_pipeline.py
│   ├── tasks_throughput_pipeline.py
│   ├── task_backlog_pipeline.py
│   └── task_response_time_pipeline.py
├── repositories/
│   └── task_metrics_repository.py
├── routes/
│   └── task_metrics_routes.py
├── schemas/
│   ├── task_metrics_schemas.py
│   ├── task_priority_schemas.py
│   ├── task_average_time_schemas.py
│   ├── task_throughput_schemas.py
│   └── task_response_time_schemas.py
├── services/
│   └── task_metrics_service.py
├── database.py
└── main.py
```

---

## Integração com Next.js

### Configuração

No projeto Next.js, crie um arquivo `.env.local`:

```env
NEXT_PUBLIC_ANALYTICS_API_URL=http://127.0.0.1:8000
```

---

### Utilitário de requisição

Crie o arquivo `lib/analyticsApi.ts`:

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

  if (!res.ok) throw new Error(`Erro ao buscar ${endpoint}: ${res.status}`);
  return res.json();
}

export const analyticsApi = {
  getByStatus:    (token: string) => fetchMetrics('/task/metrics/by-status', token),
  getByPriority:  (token: string) => fetchMetrics('/task/metrics/by-priority', token),
  getAverageTime: (token: string) => fetchMetrics('/task/metrics/average-time', token),
  getThroughput:  (token: string) => fetchMetrics('/task/metrics/throughput', token),
  getBacklog:     (token: string) => fetchMetrics('/task/metrics/backlog', token),
  getResponseTime:(token: string) => fetchMetrics('/task/metrics/response-time', token),
};
```

---

### Tipagens

Crie o arquivo `types/metrics.ts`:

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

export interface ThroughputItem {
  day: string;
  count: number;
}

export interface ThroughputResponse {
  success: boolean;
  data: ThroughputItem[];
}

export interface BacklogItem {
  date: string;
  criadas: number;
  finalizadas: number;
  backlog: number;
}

export interface BacklogResponse {
  success: boolean;
  data: BacklogItem[];
}

export interface ResponseTimeItem {
  date: string;
  slaPercentage: number;
  target: number;
}

export interface ResponseTimeResponse {
  success: boolean;
  data: ResponseTimeItem[];
}

export interface ResolutionTimeItem {
  date: string;
  onTimeSolution: number;
  target: number;
}

export interface ResolutionTimeResponse {
  success: boolean;
  data: ResolutionTimeItem[];
}
```

---

### Exemplo de uso em Server Component

```tsx
// app/dashboard/page.tsx
import { analyticsApi } from '@/lib/analyticsApi';
import { cookies } from 'next/headers';
import { MetricsByStatusResponse } from '@/types/metrics';

export default async function DashboardPage() {
  const token = cookies().get('token')?.value ?? '';

  const statusMetrics = await analyticsApi.getByStatus(token) as MetricsByStatusResponse;
  const { data } = statusMetrics;

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Total de tarefas: {data.total_tasks}</p>
      <p>Pendentes: {data.PENDING.count} ({data.PENDING.percent}%)</p>
      <p>Em andamento: {data.IN_PROGRESS.count} ({data.IN_PROGRESS.percent}%)</p>
      <p>Concluídas: {data.DONE.count} ({data.DONE.percent}%)</p>
      <p>Canceladas: {data.CANCELLED.count} ({data.CANCELLED.percent}%)</p>
    </div>
  );
}
```

---

### Exemplo de uso em Client Component com SWR

```bash
npm install swr
```

```tsx
// components/MetricsByStatus.tsx
'use client';

import useSWR from 'swr';
import { MetricsByStatusResponse } from '@/types/metrics';

const fetcher = (url: string, token: string) =>
  fetch(url, { headers: { Authorization: `Bearer ${token}` } }).then(r => r.json());

export default function MetricsByStatus({ token }: { token: string }) {
  const { data, error, isLoading } = useSWR<MetricsByStatusResponse>(
    [`${process.env.NEXT_PUBLIC_ANALYTICS_API_URL}/task/metrics/by-status`, token],
    ([url, t]) => fetcher(url, t)
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

### Tratamento de erros de autenticação

```ts
// lib/analyticsApi.ts — tratamento de 401
if (res.status === 401) {
  // Redirecionar para login
  throw new Error('Token expirado ou inválido');
}
```

No Next.js com `middleware.ts`, você pode interceptar respostas 401 e redirecionar automaticamente:

```ts
// middleware.ts
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

## Observações

- O token JWT deve ser armazenado em cookie `httpOnly` para maior segurança, evitando acesso via JavaScript
- Em produção, substitua `http://127.0.0.1:8000` pela URL real da API no `.env.local`
- Utilize `cache: 'no-store'` nas requisições de métricas para garantir dados sempre atualizados
