# Agent Fundamentals

## 1. Agent vs Chatbot vs Pipeline

| Concept      | Description                                                                                                                                                      |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chatbot**  | Responds to user queries using predefined rules or learned patterns. Primarily focused on conversation and reactive replies.                                     |
| **Pipeline** | Executes a fixed, predefined sequence of steps. The workflow is deterministic and does not change based on intermediate results.                                 |
| **Agent**    | Operates autonomously by deciding **what action to take**, **which tool to use**, and **in what order**. Adapts its behavior based on observations and feedback. |

---

## 2. Agent Architecture

```
Goal → LLM → Action/Tool → Observation → Reasoning → (Loop)
```

* **Goal:** The objective the agent is trying to achieve.
* **LLM:** Performs reasoning, planning, and decision-making.
* **Action / Tool:** Any executable capability (e.g., code execution, database query, API call).
* **Observation:** The result returned by the tool or environment.
* **Loop:** The agent iteratively reasons over observations until the goal is satisfied or a stopping condition is met.

---

## 3. ReAct Pattern

**ReAct = Reason → Act → Observe → Reason**

* **Reason:** Analyze the current state and decide the next step.
* **Act:** Execute an action using an appropriate tool.
* **Observe:** Capture the result of the action.
* **Iterate:** Use the observation to inform the next reasoning step.

This pattern tightly couples reasoning with actions, enabling dynamic and adaptive behavior.

---

## 4. Role Isolation

* Each agent has a **single, well-defined responsibility**.
* Prevents role leakage, conflicts, and unintended behavior.
* Improves reliability and debuggability in multi-agent systems.

**Examples:**

| Agent Type       | Responsibility                          | Restrictions                                                   |
| ---------------- | --------------------------------------- | -------------------------------------------------------------- |
| **Researcher**   | Gathers and verifies information        | Must **not summarize** or answer the user’s question           |
| **Summarizer**   | Condenses and structures information    | Must **not provide final answers**                             |
| **Answer Agent** | Produces the final user-facing response | Uses upstream outputs only; does **not research or summarize** |

---

## 5. System Prompts

* Define an agent’s **behavior, scope, and constraints**.
* Enforce role isolation and prevent overreach.
* Act as a contract that the agent must follow.

**Examples:**

* *Researcher:* "Collect relevant information for the task. Do not answer the user’s question."
* *Summarizer:* "Summarize the provided information. Do not add new facts or answer questions."

---

## 6. Message-Based Communication

* Agents interact via **structured messages**, not shared state.
* Supports modular, scalable, and asynchronous coordination.

**Typical message fields:**

* **Content:** The data or instruction being sent.
* **Source:** The sender (user or agent).
* **Metadata:** Task ID, message type, constraints, or routing information.
