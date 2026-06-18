# Guia de Implementação: Gráfico de Produtividade (Histórico vs. Previsão)

Este documento orienta a implementação de um gráfico de linha comparativo no frontend Next.js, integrando dados reais de throughput e projeções de machine learning.

## 1. Endpoints de Dados

Para construir o gráfico, o agente deve consumir dois endpoints da API de Analytics:

### A. Histórico de Produtividade (Linha 1)
- **Rota:** `GET /task/metrics/throughput`
- **Descrição:** Retorna a quantidade de tarefas concluídas por dia.
- **Formato da Resposta:**
```json
{
  "success": true,
  "data": [
    { "date": "2023-10-01", "count": 5 },
    { "date": "2023-10-02", "count": 8 }
  ]
}
```

### B. Previsão de Produtividade (Linha 2)
- **Rota:** `GET /task/predictions/throughput`
- **Descrição:** Retorna a projeção para os próximos 7 dias.
- **Formato da Resposta:**
```json
{
  "success": true,
  "data": {
    "forecast": [
      { "day": "2023-10-03", "count": 6 },
      { "day": "2023-10-04", "count": 7 }
    ]
  }
}
```

## 2. Lógica de Processamento de Dados

Como os endpoints possuem chaves de data diferentes (`date` vs `day`), o frontend deve normalizar os dados antes de passá-los para o componente `LineChart`.

**Regras de Negócio:**
1. Unificar as listas em um único array de objetos.
2. Usar uma chave comum (ex: `name` ou `displayDate`) para o eixo X.
3. Manter as chaves `actual` (para o histórico) e `forecast` (para a previsão) separadas para que o Recharts renderize duas linhas independentes.
4. Ordenar o array final por data cronológica.

## 3. Exemplo de Implementação (React + Recharts)

```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ProductivityChart = ({ historicalData, forecastData }) => {
  // Transformação para o formato do Recharts
  const chartData = [
    ...historicalData.map(item => ({
      day: item.date,
      actual: item.count
    })),
    ...forecastData.map(item => ({
      day: item.day,
      forecast: item.count
    }))
  ].sort((a, b) => new Date(a.day).getTime() - new Date(b.day).getTime());

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="day" 
          tickFormatter={(str) => new Date(str).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })}
        />
        <YAxis />
        <Tooltip />
        <Legend />
        
        {/* Linha 1: Histórico Real */}
        <Line
          type="monotone"
          dataKey="actual"
          name="Real"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={{ r: 4 }}
          connectNulls
        />

        {/* Linha 2: Previsão (Tracejada) */}
        <Line
          type="monotone"
          dataKey="forecast"
          name="Previsão"
          stroke="#10b981"
          strokeDasharray="5 5"
          strokeWidth={2}
          dot={{ r: 4 }}
          connectNulls
        />
      </LineChart>
    </ResponsiveContainer>
  );
};
```

## 4. Recomendações de UI/UX

- **Cores:** Utilize cores contrastantes (ex: Azul para Real, Verde para Previsão).
- **Estilo:** A linha de previsão deve ser obrigatoriamente tracejada (`strokeDasharray`) para indicar que são dados não confirmados.
- **Interatividade:** O `Tooltip` deve ser configurado para mostrar a data completa formatada e o valor exato daquela métrica.
- **Estado Vazio:** Se `forecastData` estiver vazio (mínimo de 7 dias de histórico não atingido), exibir uma mensagem informativa ao usuário.

---
*Documentação gerada para suporte ao desenvolvimento do Squad de Analytics - TaskInsight.*