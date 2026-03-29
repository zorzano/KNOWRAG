# KNOWRAG

KNOWRAG is an experimental framework for the systematic design and evaluation of Retrieval-Augmented Generation (RAG) systems over Knowledge Graphs (KGs).

This repository accompanies the research work:

**"KNOWRAG: Systematic Design and Evaluation of Knowledge Graph–Based Retrieval-Augmented Generation"**

The framework enables controlled experimentation with different RAG configurations, including:
- LLM-driven query generation
- Multi-node graph retrieval
- Iterative retrieval refinement
- LLM-based answer generation and evaluation

Experiments are conducted over:
- **KITI**: an industrial IoT Knowledge Graph
- **IRN**: an external benchmark based on World Cup data

---

## Repository Structure

```
rag/
 ├── executeExperimentKITI.sh
 ├── executeExperimentIRN.sh
 ├── C0xx/                  # KITI experiments
 │    └── config.txt
 ├── C3xx/                  # IRN experiments
 │    └── config.txt
repo/
 └── code/                  # Core Python implementation
```

Each experiment is defined by a configuration file (`config.txt`) that specifies:
- RAG components (A, B, C, D)
- Parameters (k, m, n)
- Model configuration

---

## Requirements

- Ubuntu (tested on AWS t2.small)
- Python 3.10
- Neo4j (5.x recommended)
- OpenAI API access

---

## Environment Setup

### 1. Create machine

Recommended:
- AWS EC2 instance (t2.small)
- Ubuntu
- 20GB disk

---

### 2. Install Neo4j

```bash
sudo apt-get install wget curl nano software-properties-common dirmngr apt-transport-https gnupg gnupg2 ca-certificates lsb-release ubuntu-keyring unzip -y

curl -fsSL https://debian.neo4j.com/neotechnology.gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/neo4j.gpg

echo "deb [signed-by=/usr/share/keyrings/neo4j.gpg] https://debian.neo4j.com stable latest" | sudo tee -a /etc/apt/sources.list.d/neo4j.list

sudo apt-get update
sudo apt-get install neo4j -y

sudo systemctl enable --now neo4j
```

---

### 3. Configure Neo4j

Connect:

```bash
cypher-shell -a 'neo4j://127.0.0.1:7687' -u neo4j -p neo4j
```

Change default password when prompted.

Create vector index:

```cypher
CREATE VECTOR INDEX allembeddings IF NOT EXISTS
FOR (m:Searchable)
ON m.embedding
OPTIONS {
  indexConfig: {
    `vector.dimensions`: 1536,
    `vector.similarity_function`: 'cosine'
  }
};
```

---

### 4. Install Python dependencies

```bash
sudo apt install python3-pip

pip install -U pip setuptools wheel
pip install neo4j
pip install spacy
python3 -m spacy download es_core_news_sm
pip install openai
pip install tiktoken
```

---

### 5. Environment variables

Set the following variables (e.g., in `.bashrc`):

```bash
export PWDNEO4J=your_password
export OPENAI_API_KEY=your_api_key
```

---

## Running the Experiments

### Grant execution permissions

```bash
chmod +x rag/executeExperimentKITI.sh
chmod +x rag/executeExperimentIRN.sh
```

---

### Run KITI experiments

```bash
cd rag
./executeExperimentKITI.sh
```

---

### Run IRN experiments

```bash
cd rag
./executeExperimentIRN.sh
```

---

## What the scripts do

Both scripts:

1. Reset and reload the Neo4j database
2. Execute all experiment configurations sequentially
3. Collect results from each experiment
4. Generate a final summary file:

```
out.txt
```

This file contains aggregated metrics such as:
- Number of questions
- Token usage
- Execution time
- Evaluation scores (1–5 scale)

---

## Configuration System

Each experiment is defined in:

```
rag/Cxxx/config.txt
```

Where:
- `C0xx` → KITI experiments
- `C3xx` → IRN experiments

Configurations specify:
- Active components: {A, B, C, D}
- Parameters: k, m, n
- Model selection

---

## Data Availability
The file "Knowledge Graphs employed in the experiments.pdf" contains a description of the Knowledge Graphs structures.

### IRN dataset

The corrected IRN benchmark is publicly available and included (or reproducible from its original source).

---

### KITI dataset

Due to privacy constraints, the KITI dataset included in this repository contains only a subset of the original data.

To reproduce the full experiments, please contact the repository owner.

---

## Unit Tests

Basic functionality can be validated with:

```bash
export PWDNEO4J=your_password

python3 TestKGIoTDriver.py
python3 repo/code/TestGordopiloDialog.py
python3 TestGordopiloDialog.py TestGordopiloDialog.test_02
```

---

## Notes on Models

- OpenAI API access is required
- Model selection is defined per experiment (`config.txt`)
- The evaluator uses a fixed GPT-4-class model internally

---

## Reproducibility Notes

- Results depend on:
  - LLM version
  - API behavior
  - Dataset completeness (KITI full vs partial)
- Token usage and execution time may vary

---

## License

(To be defined)

---

## Contact

For dataset access or questions, please contact the repository owner.
