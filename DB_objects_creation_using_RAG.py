{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "78df1dd8-6690-455b-bbd8-98c0147a69d1",
   "metadata": {},
   "outputs": [],
   "source": [
    "from pathlib import Path\n",
    "from autogen import AssistantAgent\n",
    "from autogen import initiate_chats\n",
    "from db_config import connect_db\n",
    "from autogen.coding import  CodeBlock, LocalCommandLineCodeExecutor\n",
    "from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent\n",
    "from autogen.retrieve_utils import TEXT_FORMATS,extract_text_from_pdf\n",
    "work_dir = Path(\"coding_RAG\")\n",
    "work_dir.mkdir(exist_ok=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "a0f9ca72-763b-489f-92a3-7f96b73aaffc",
   "metadata": {},
   "outputs": [],
   "source": [
    "llm_config = {\"model\": \"gemini-3.1-flash-lite\",\"api_key\":\"\",\"api_type\":\"google\"}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "bc3e7f5f-6466-4cbf-9074-629f7875b7f9",
   "metadata": {},
   "outputs": [],
   "source": [
    "executor = LocalCommandLineCodeExecutor(work_dir=work_dir)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "8f3fe247-0d89-439c-b1a1-19bf0e25631f",
   "metadata": {},
   "outputs": [],
   "source": [
    "assistant = AssistantAgent(\n",
    "    name=\"assistant\",\n",
    "    system_message=\"\"\"You are helpful Database developer.\n",
    "        You are required to connect to the database.\n",
    "        Create the mentioned tables in the database and insert the data into the tables\n",
    "        You are a helpful Database connection agent.\n",
    "    Connect MYSQL Database using db_config.py import connect_db function\"\"\",\n",
    "    llm_config=llm_config,\n",
    "    code_execution_config={\n",
    "        \"executor\": executor,\n",
    "    },\n",
    "    max_consecutive_auto_reply=1\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "0dae536b-6c6f-4ade-8100-6f2c20f30daa",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Accepted file formats for `docs_path`:\n",
      "['txt', 'json', 'csv', 'tsv', 'md', 'html', 'htm', 'rtf', 'rst', 'jsonl', 'log', 'xml', 'yaml', 'yml', 'pdf', 'mdx']\n"
     ]
    }
   ],
   "source": [
    "print(\"Accepted file formats for `docs_path`:\")\n",
    "print(TEXT_FORMATS)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "4d8b8791-6806-457e-bb6e-58eb2407309d",
   "metadata": {},
   "outputs": [],
   "source": [
    "pdf_files = [\"Create University Database Design document.pdf\"]\n",
    "docs_content= extract_text_from_pdf(\"Create University Database Design document.pdf\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "0bc517da-0b0e-44c0-80c6-6a8b1101447c",
   "metadata": {},
   "outputs": [],
   "source": [
    "ragproxyagent = RetrieveUserProxyAgent(\n",
    "    name=\"ragproxyagent\",\n",
    "    human_input_mode=\"NEVER\",\n",
    "    max_consecutive_auto_reply=1,\n",
    "    retrieve_config={\n",
    "        \"task\": \"qa\",\n",
    "        \"docs_path\": [\"RAG/Create University Database Design document.pdf\"],\n",
    "        \"docs_content\": docs_content,  # Provide the extracted content directly\n",
    "        \"chunk_token_size\": 200,\n",
    "        \"model\": \"gemini-3.1-flash-lite\",\n",
    "        \"vector_db\": \"chroma\",\n",
    "        \"overwrite\": True,\n",
    "        \"get_or_create\": True,\n",
    "    },\n",
    "    code_execution_config={\n",
    "        \"executor\": executor,\n",
    "    },\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "7033e45a-af17-4df0-b28f-8826584d1455",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Trying to create collection.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "max_tokens is too small to fit a single line of text. Breaking this line:\n",
      "\t   ...\n",
      "Failed to split docs with must_break_at_empty_line being True, set to False.\n",
      "2026-05-30 19:12:27,255 - autogen.agentchat.contrib.retrieve_user_proxy_agent - INFO - Found 6 chunks.\u001b[0m\n",
      "2026-05-30 19:12:27,290 - autogen.agentchat.contrib.vectordb.chromadb - INFO - No content embedding is provided. Will use the VectorDB's embedding function to generate the content embedding.\u001b[0m\n",
      "Model gemini-3.1-flash-lite not found. Using cl100k_base encoding.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "VectorDB returns doc_ids:  [['8be20fc1', 'a7b6652f', '967b2b49', '980f2006', '47bb2d59', 'ff528335']]\n",
      "\u001b[32mAdding content of doc 8be20fc1 to context.\u001b[0m\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Model gemini-3.1-flash-lite not found. Using cl100k_base encoding.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[32mAdding content of doc a7b6652f to context.\u001b[0m\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Model gemini-3.1-flash-lite not found. Using cl100k_base encoding.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[32mAdding content of doc 967b2b49 to context.\u001b[0m\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Model gemini-3.1-flash-lite not found. Using cl100k_base encoding.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[32mAdding content of doc 980f2006 to context.\u001b[0m\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Model gemini-3.1-flash-lite not found. Using cl100k_base encoding.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[32mAdding content of doc 47bb2d59 to context.\u001b[0m\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Model gemini-3.1-flash-lite not found. Using cl100k_base encoding.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[32mAdding content of doc ff528335 to context.\u001b[0m\n",
      "\u001b[33mragproxyagent\u001b[0m (to assistant):\n",
      "\n",
      "You're a retrieve augmented chatbot. You answer user's questions based on your own knowledge and the\n",
      "context provided by the user.\n",
      "If you can't answer the question with or without the current context, you should reply exactly `UPDATE CONTEXT`.\n",
      "You must give as short an answer as possible.\n",
      "\n",
      "User's question is: Connect to DB and create the mentioned tables and data present in the document\n",
      "\n",
      "Context is: Create University Database Design document  \n",
      "  \n",
      "1. Department Table (departments)  \n",
      "Column Name  Data Type  Descripti \n",
      "Constraints on  \n",
      "dept_id  INT  PRIMARY KEY ,  \n",
      "AUTO_INCRE \n",
      "MENT  \n",
      "Unique  \n",
      "identifier  \n",
      "for each \n",
      "departm \n",
      "ent  \n",
      "dept_name  NOT NULL, \n",
      "VARCHAR(100)  \n",
      "UNIQUE  \n",
      "Full  \n",
      "name of \n",
      "the  \n",
      "departm \n",
      "ent  \n",
      "building  VARCHAR(50)  NOT NULL  Campus \n",
      "location \n",
      "or \n",
      "building \n",
      "name  \n",
      "Annual  \n",
      "departm \n",
      "CHECK (budget  \n",
      "budget  DECIMAL(12,2)  ent  \n",
      "> 0)  \n",
      "budget \n",
      "in ₹  \n",
      "2. Courses Table (courses)  \n",
      "Department table data:  \n",
      "214  \n",
      "dept_id   dept_name       building    budget  \n",
      "101  Computer Science & Engineering  Ramanujan Block  1500000.00  \n",
      "102  Mechanical Engineering      Kalam Labs    1200000.00  \n",
      "103  Electrical & Electronics      Tesla Pavilion    950000.00  \n",
      "104  Business Administration     Aryabhata Hall   800000.00  \n",
      "  \n",
      "Courses table data:  \n",
      "course_id title  credits dept_id  \n",
      "CS101  Introduction to Python  4  101  \n",
      "CS202  Database Management Systems 4  101  ME105  Engineering Graphics  3  102  \n",
      "EE210  Circuit Theory  4  103  \n",
      "BA101  Principles of Management  3  104\n",
      "5)  \n",
      "NOT NULL  Contact \n",
      "phone \n",
      "number  \n",
      "enroll_da \n",
      "DATE  \n",
      "te  \n",
      "DEFAULT \n",
      "(CURRENT_DATE) \n",
      "Date the \n",
      "student \n",
      "joined the \n",
      "university  \n",
      "FOREIGN KEY \n",
      "references Major \n",
      "choice  \n",
      "dept_id  INT  \n",
      "departments(dept department  \n",
      "_id)  \n",
      "  \n",
      "  Students \n",
      "table \n",
      "data:  \n",
      "  first_nam last_nam email  phone  \n",
      " e  e  enroll_date  dept_id  \n",
      "  \n",
      "student_id  \n",
      "2026001  Sairam  Krishnan  sairam.k@univ.ed \n",
      "  \n",
      "3. Student Table (students)  \n",
      "Column  \n",
      "Data Type  Constraints  Description Name  \n",
      "student_i \n",
      "INT  \n",
      "d  \n",
      "PRIMARY KEY  Unique \n",
      "registration \n",
      "roll number  \n",
      "first_nam \n",
      "VARCHAR(5 \n",
      "e  0)  \n",
      "NOT NULL  First name \n",
      "of the \n",
      "student  \n",
      "last_nam \n",
      "VARCHAR(5 \n",
      "e  0)  \n",
      "NOT NULL  Last  \n",
      "name/Surna \n",
      "me of the \n",
      "student  \n",
      "VARCHAR(1 \n",
      "email  \n",
      "00)  \n",
      "NOT NULL,  \n",
      "UNIQUE  \n",
      "Official \n",
      "university \n",
      "email \n",
      "address  \n",
      "VARCHAR(1 \n",
      "phone  \n",
      "  \n",
      "Column \n",
      "Name  Data Type  Constraints  Descripti \n",
      "on  \n",
      "course \n",
      "_id  \n",
      "VARCHAR( \n",
      "10)  PRIMARY KEY  \n",
      "Unique \n",
      "academic  \n",
      "code  \n",
      "(e.g.,  \n",
      "CS101)  \n",
      "title  VARCHAR( \n",
      "100)  NOT NULL  \n",
      "Name of \n",
      "the \n",
      "course  \n",
      "credits  INT  CHECK (credits  \n",
      "BETWEEN 1 AND 5)  \n",
      "Academi \n",
      "c credit \n",
      "weight   FOREIGN KEY  The  \n",
      "dept_id INT  references  offering  \n",
      "departments(dep departme \n",
      "t_id) nt  \n",
      "u  \n",
      "9876543 \n",
      "210  \n",
      "2026-06-01  101  \n",
      "2026002  Abami  Priya  abami.p@univ.ed \n",
      "u  \n",
      "9876543 \n",
      "211  \n",
      "2026-06-01  101  \n",
      "2026003  Rahul  Sharma  rahul.s@univ.edu  9876543 \n",
      "212  \n",
      "2026-06-02  102  \n",
      "2026004  Meera  Nair  meera.n@univ.ed \n",
      "u  \n",
      "9876543 \n",
      "213  \n",
      "2026-06-03  103  \n",
      "vikram.s@univ.ed 9876543 \n",
      "2026005  Vikram  Singh  2026-06-05  104  \n",
      "u  \n",
      "  \n",
      "\n",
      "\n",
      "\n",
      "--------------------------------------------------------------------------------\n",
      "\u001b[33massistant\u001b[0m (to ragproxyagent):\n",
      "\n",
      "```python\n",
      "from db_config import connect_db\n",
      "\n",
      "def setup_university_db():\n",
      "    conn = connect_db()\n",
      "    cursor = conn.cursor()\n",
      "\n",
      "    # Create Tables\n",
      "    cursor.execute(\"DROP TABLE IF EXISTS students, courses, departments\")\n",
      "    \n",
      "    cursor.execute(\"\"\"\n",
      "        CREATE TABLE departments (\n",
      "            dept_id INT PRIMARY KEY AUTO_INCREMENT,\n",
      "            dept_name VARCHAR(100) UNIQUE NOT NULL,\n",
      "            building VARCHAR(50) NOT NULL,\n",
      "            budget DECIMAL(12,2) CHECK (budget > 0)\n",
      "        )\n",
      "    \"\"\")\n",
      "\n",
      "    cursor.execute(\"\"\"\n",
      "        CREATE TABLE courses (\n",
      "            course_id VARCHAR(10) PRIMARY KEY,\n",
      "            title VARCHAR(100) NOT NULL,\n",
      "            credits INT CHECK (credits BETWEEN 1 AND 5),\n",
      "            dept_id INT,\n",
      "            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)\n",
      "        )\n",
      "    \"\"\")\n",
      "\n",
      "    cursor.execute(\"\"\"\n",
      "        CREATE TABLE students (\n",
      "            student_id INT PRIMARY KEY,\n",
      "            first_name VARCHAR(50) NOT NULL,\n",
      "            last_name VARCHAR(50) NOT NULL,\n",
      "            email VARCHAR(100) UNIQUE NOT NULL,\n",
      "            phone VARCHAR(15) NOT NULL,\n",
      "            enroll_date DATE DEFAULT (CURRENT_DATE),\n",
      "            dept_id INT,\n",
      "            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)\n",
      "        )\n",
      "    \"\"\")\n",
      "\n",
      "    # Insert Data\n",
      "    cursor.executemany(\"INSERT INTO departments VALUES (%s, %s, %s, %s)\", [\n",
      "        (101, 'Computer Science & Engineering', 'Ramanujan Block', 1500000.00),\n",
      "        (102, 'Mechanical Engineering', 'Kalam Labs', 1200000.00),\n",
      "        (103, 'Electrical & Electronics', 'Tesla Pavilion', 950000.00),\n",
      "        (104, 'Business Administration', 'Aryabhata Hall', 800000.00)\n",
      "    ])\n",
      "\n",
      "    cursor.executemany(\"INSERT INTO courses VALUES (%s, %s, %s, %s)\", [\n",
      "        ('CS101', 'Introduction to Python', 4, 101),\n",
      "        ('CS202', 'Database Management Systems', 4, 101),\n",
      "        ('ME105', 'Engineering Graphics', 3, 102),\n",
      "        ('EE210', 'Circuit Theory', 4, 103),\n",
      "        ('BA101', 'Principles of Management', 3, 104)\n",
      "    ])\n",
      "\n",
      "    cursor.executemany(\"INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s)\", [\n",
      "        (2026001, 'Sairam', 'Krishnan', 'sairam.k@univ.edu', '9876543210', '2026-06-01', 101),\n",
      "        (2026002, 'Abami', 'Priya', 'abami.p@univ.edu', '9876543211', '2026-06-01', 101),\n",
      "        (2026003, 'Rahul', 'Sharma', 'rahul.s@univ.edu', '9876543212', '2026-06-02', 102),\n",
      "        (2026004, 'Meera', 'Nair', 'meera.n@univ.edu', '9876543213', '2026-06-03', 103),\n",
      "        (2026005, 'Vikram', 'Singh', 'vikram.s@univ.edu', '9876543214', '2026-06-05', 104)\n",
      "    ])\n",
      "\n",
      "    conn.commit()\n",
      "    cursor.close()\n",
      "    conn.close()\n",
      "\n",
      "setup_university_db()\n",
      "```\n",
      "\n",
      "--------------------------------------------------------------------------------\n",
      "\u001b[31m\n",
      ">>>>>>>> EXECUTING CODE BLOCK (inferred language is python)...\u001b[0m\n",
      "\u001b[33mragproxyagent\u001b[0m (to assistant):\n",
      "\n",
      "exitcode: 0 (execution succeeded)\n",
      "Code output: \n",
      "\n",
      "--------------------------------------------------------------------------------\n",
      "\u001b[31m\n",
      ">>>>>>>> TERMINATING RUN (c9b4bea5-828c-4161-a4e7-675d88490e50): Maximum number of consecutive auto-replies reached\u001b[0m\n"
     ]
    }
   ],
   "source": [
    "qa_problem = \"Connect to DB and create the mentioned tables and data present in the document\"\n",
    "chat_result = ragproxyagent.initiate_chat(assistant, message=ragproxyagent.message_generator, problem=qa_problem)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e4128075-8b29-40db-8c29-36a8d259e9ea",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (agenticai)",
   "language": "python",
   "name": "agenticai"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
