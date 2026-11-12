# Google ADK'ga o'tish (keyingi bosqich)
Hozirgi agentlar qoidalarga asoslangan (deterministik, test qilish oson).
Keyingi bosqichda har bir agent `google.adk.agents.LlmAgent` ga o'raladi,
`ai_agents/` dagi funksiyalar esa agent *tools* sifatida beriladi.
Koordinator `SequentialAgent` / `ParallelAgent` bilan quriladi.
