# Dokumentim Akademik i Projektit LogicLab

## 1. Titulli i Projektit

**LogicLab: Platformë Web për Analizë Booleane, Qarqe Digjitale, Algoritme dhe Tutorim me Inteligjencë Artificiale**

## 2. Abstrakt

LogicLab është një platformë edukative e ndërtuar me Django që integron koncepte nga Matematika Diskrete, Logjika Digjitale, Algoritmet dhe Programimi i Avancuar, Programimi në Web dhe Inteligjenca Artificiale e Aplikuar. Projekti synon të krijojë një mjedis praktik ku studenti mund të analizojë shprehje Booleane, të gjenerojë tabela të së vërtetës, të studiojë strukturën e qarqeve logjike, të kuptojë kompleksitetin algoritmik dhe të përdorë një Tutor AI lokal për shpjegime teorike dhe analizë imazhesh.

Në nivel teknik, projekti është ndërtuar mbi arkitekturën Model-View-Template të Django-s, përdor SymPy për përpunimin simbolik të shprehjeve Booleane, SQLite për ruajtjen e historikut dhe Ollama për integrimin e një modeli lokal AI. Moduli Algorithm Lab zgjeron projektin me analiza Big O, Big Θ dhe Big Ω, visualizer të algoritmeve të renditjes, demonstrime rekursioni dhe teori algoritmike të strukturuar.

## 3. Qëllimi i Projektit

Qëllimi kryesor i LogicLab është të shërbejë si një laborator interaktiv akademik për lidhjen e teorisë me praktikën. Projekti nuk kufizohet vetëm në analizimin e shprehjeve Booleane, por e zgjeron atë analizë drejt implementimit digjital, kompleksitetit algoritmik dhe asistencës me AI.

Objektivat kryesore janë:

- të analizohen shprehje Booleane në mënyrë automatike;
- të gjenerohen tabela të së vërtetës për variablat e dhëna;
- të thjeshtohen shprehjet me metoda simbolike;
- të gjenerohen forma kanonike SOP dhe POS;
- të numërohen portat logjike të nevojshme për qarkun;
- të shpjegohet struktura e qarkut në mënyrë të kuptueshme;
- të lidhet analiza Booleane me kompleksitetin algoritmik `O(2^n)`;
- të ofrohet laborator për algoritme, sorting dhe rekursion;
- të përdoret AI lokale për tutorim akademik dhe analizë imazhesh.

## 4. Lëndët e Integruara

### 4.1 Matematika Diskrete

Matematika Diskrete përfaqëson bazën teorike të projektit. Në LogicLab ajo shfaqet përmes algjebrës Booleane, tabelave të së vërtetës, tautologjive, kontradiktave, kontingjencave dhe formave kanonike SOP/POS.

Përdoruesi shkruan një shprehje si:

```text
(A & B) | (~A & C)
```

Sistemi e normalizon, e analizon dhe e përkthen në një strukturë të vlerësueshme matematikisht.

### 4.2 Logjika Digjitale

Logjika Digjitale lidhet me interpretimin praktik të shprehjeve Booleane si qarqe kombinacionale. Çdo operator logjik mund të përfaqësohet nga një portë digjitale:

- `NOT` për mohimin;
- `AND` për konjunksionin;
- `OR` për disjunksionin;
- `XOR` për ekskluzivitetin logjik.

Në faqen e rezultatit, projekti shfaq “Struktura e Qarkut”, ku përdoruesi sheh hyrjet, portat e përdorura dhe daljen finale `F`.

### 4.3 Algoritme dhe Programim i Avancuar

Moduli Algorithm Lab integron konceptet kryesore të analizës algoritmike. Përmes këtij moduli, studenti mund të studiojë:

- Big O, Big Θ dhe Big Ω;
- cikle të folezuara;
- rekursion dhe iteracion;
- Insertion Sort;
- Selection Sort;
- Quick Sort;
- Merge Sort;
- Divide and Conquer;
- Greedy Algorithms;
- Dynamic Programming;
- Linked List;
- Binary Search;
- Memoization.

Një lidhje e rëndësishme me LogicLab është analiza e tabelës së së vërtetës. Për `n` variabla, ekzistojnë `2^n` kombinime të mundshme, prandaj gjenerimi i tabelës ka kompleksitet:

```text
O(2^n)
```

### 4.4 Programim në Web me Django

Projekti demonstron ndërtimin e një aplikacioni web modular me Django. Ai përdor:

- apps të ndara sipas funksionalitetit;
- URL routing të organizuar;
- views për përpunimin e kërkesave;
- templates për ndërfaqen;
- forms për input të përdoruesit;
- models për ruajtjen e të dhënave;
- engine files për logjikën e biznesit.

Kjo ndarje e bën projektin më të mirëorganizuar, më të lehtë për mirëmbajtje dhe më të zgjerueshëm.

### 4.5 Inteligjencë Artificiale e Aplikuar

Tutor AI përdor Ollama për të ekzekutuar një model lokal. Modeli aktual i konfiguruar është:

```text
granite3.2-vision:2b
```

Ky model mbështet analizë teksti dhe imazhesh, duke e bërë të mundur që përdoruesi të bëjë pyetje për logjikë, algoritme dhe qarqe digjitale. Tutor AI është i kufizuar në temat akademike të projektit dhe përgjigjet në anglisht profesionale.

## 5. Arkitektura e Projektit

LogicLab përdor arkitekturën tipike të Django-s, e cila ndahet në disa shtresa:

- **Presentation Layer:** templates HTML me Bootstrap;
- **Routing Layer:** skedarët `urls.py`;
- **Controller Layer:** views Django;
- **Business Logic Layer:** engine files;
- **Data Layer:** models dhe SQLite;
- **AI Integration Layer:** komunikim me Ollama API.

Struktura kryesore:

```text
logiclab/
├── analyzer/
├── algorithms/
├── chatbot/
├── uploads/
├── logiclab/
├── templates/
├── static/
├── media/
├── requirements.txt
├── manage.py
└── README.md
```

## 6. Përshkrimi Teknik i Moduleve

## 6.1 Moduli Analyzer

Moduli `analyzer` është përgjegjës për analizimin e shprehjeve Booleane.

Skedarët kryesorë:

- `logic_engine.py`
- `circuit_generator.py`
- `views.py`
- `forms.py`
- `models.py`

Funksionet kryesore të `logic_engine.py` përfshijnë:

- normalizimin e shprehjes;
- nxjerrjen e variablave;
- parsing të shprehjes me SymPy;
- gjenerimin e tabelës së së vërtetës;
- thjeshtimin e shprehjes;
- gjenerimin e formave SOP/POS;
- klasifikimin logjik;
- analizën algoritmike të tabelës së së vërtetës.

Shembull i analizës algoritmike:

```python
algorithm_analysis = {
    "variable_count": len(variables),
    "combination_count": 2 ** len(variables),
    "time_complexity": "O(2^n)",
    "space_complexity": "O(2^n)",
}
```

Ky rezultat shfaqet në faqen e rezultatit si pjesë e seksionit “Analizë Algoritmike”.

## 6.2 Moduli Circuit Generator

Skedari `circuit_generator.py` përkthen strukturën simbolike të shprehjes në hapa të lexueshëm qarku.

Ai kryen:

- numërimin e portave logjike;
- gjenerimin e hapave të qarkut;
- krijimin e DOT source për përdorim të mundshëm grafik në të ardhmen.

Në ndërfaqe nuk shfaqet më DOT source teknik. Ai është zëvendësuar me seksionin “Struktura e Qarkut”, i cili është më i kuptueshëm për përdoruesin final.

## 6.3 Moduli Algorithms

Moduli `algorithms` është ndërtuar si app i veçantë Django për lëndën Algoritme dhe Programim i Avancuar.

Skedarët kryesorë:

- `complexity_engine.py`
- `sorting_engine.py`
- `recursion_engine.py`
- `theory_data.py`
- `views.py`
- `urls.py`

### Complexity Engine

`complexity_engine.py` ruan raste të gatshme analize për pseudokode të njohura, si:

- cikle të folezuara trekëndore;
- cikle të dyfishta plus cikël linear;
- gjenerimi i tabelës së së vërtetës.

Çdo rast kthen:

- titull;
- pseudokod;
- shpjegim;
- Big O;
- Big Θ;
- Big Ω;
- shënim efikasiteti.

### Sorting Engine

`sorting_engine.py` implementon algoritme renditjeje dhe gjeneron hapa të ndërmjetëm për secilin algoritëm.

Algoritmet e mbështetura janë:

- Insertion Sort;
- Selection Sort;
- Quick Sort;
- Merge Sort.

Çdo algoritëm kthen:

- listën fillestare;
- listën finale;
- hapat;
- numrin e krahasimeve;
- numrin e swaps;
- numrin e shifts;
- kompleksitetet best, average dhe worst case.

### Recursion Engine

`recursion_engine.py` demonstron ndryshimin midis faktorialit rekursiv dhe atij iterativ.

Ai tregon:

- rezultatin;
- numrin e thirrjeve rekursive;
- numrin e iterimeve;
- kompleksitetin kohor;
- kompleksitetin hapësinor;
- lidhjen me pemët e shprehjeve Booleane.

### Theory Data

`theory_data.py` ruan tema teorike të strukturuara, të cilat shfaqen në faqen Theory si accordion Bootstrap.

## 6.4 Moduli Chatbot

Moduli `chatbot` ofron Tutor AI.

Skedarët kryesorë:

- `ai_engine.py`
- `forms.py`
- `views.py`
- `urls.py`

`ai_engine.py` komunikon me Ollama përmes endpoint-it:

```text
/api/chat
```

Ai dërgon:

- system prompt;
- pyetjen e përdoruesit;
- imazhin në base64 nëse ekziston;
- opsione si `temperature`, `top_p`, `num_ctx` dhe `num_predict`.

Nëse Ollama nuk përgjigjet, përdoret fallback demo.

## 6.5 Moduli Uploads

Moduli `uploads` lejon ngarkimin e imazheve të qarqeve logjike.

Ai përdor:

- `CircuitImage` model;
- `CircuitImageForm`;
- `analyze_uploaded_image`;
- Tutor AI për interpretim të imazhit.

Imazhi ruhet në `media/`, ndërsa shpjegimi ruhet në fushën `ai_explanation`.

## 7. Modelet e të Dhënave

Projekti përdor SQLite si databazë zhvillimi.

### BooleanExpression

Modeli `BooleanExpression` ruan:

- shprehjen origjinale;
- shprehjen e normalizuar;
- shprehjen e thjeshtuar;
- variablat;
- tipin e shprehjes;
- numrin e portave;
- datën e krijimit.

### CircuitImage

Modeli `CircuitImage` ruan:

- titullin;
- imazhin;
- datën e upload-it;
- shpjegimin nga AI.

## 8. Ndërfaqja e Përdoruesit

Ndërfaqja është ndërtuar me Bootstrap 5 dhe Bootstrap Icons. Projekti përdor një `base.html` të përbashkët për navigim, footer dhe strukturë bazë.

Faqet kryesore:

- Kryefaqja;
- Analizuesi Boolean;
- Rezultati;
- Historiku;
- Tutor AI;
- Upload Imazhi;
- Algorithm Lab;
- Rreth Projektit.

Stili ruhet në:

```text
static/css/style.css
```

## 9. Konfigurimi i AI

Konfigurimi i Ollama ruhet në `.env`:

```env
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=granite3.2-vision:2b
OLLAMA_TIMEOUT=120
OLLAMA_NUM_CTX=2048
OLLAMA_NUM_PREDICT=500
OLLAMA_IMAGE_MAX_SIDE=768
```

Për të shkarkuar modelin:

```bash
ollama pull granite3.2-vision:2b
```

Imazhet zvogëlohen para dërgimit te Ollama për të ulur përdorimin e resurseve.

## 10. Siguria dhe Kufizimet

Projekti është ndërtuar për përdorim akademik dhe demonstrim lokal. Kufizimet kryesore janë:

- `DEBUG=True` në konfigurimin aktual lokal;
- SQLite përdoret për thjeshtësi zhvillimi;
- modeli AI varet nga performanca e kompjuterit lokal;
- analiza e imazheve nuk garanton saktësi nëse skema është e paqartë;
- tabela e së vërtetës kufizohet në numër të vogël variablash për shkak të kompleksitetit eksponencial.

## 11. Testimi

Testimi bazë bëhet me:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

URL-të që duhet të hapen:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/analyzer/
http://127.0.0.1:8000/history/
http://127.0.0.1:8000/chatbot/
http://127.0.0.1:8000/uploads/
http://127.0.0.1:8000/about/
http://127.0.0.1:8000/algorithms/
http://127.0.0.1:8000/algorithms/complexity/
http://127.0.0.1:8000/algorithms/sorting/
http://127.0.0.1:8000/algorithms/recursion/
http://127.0.0.1:8000/algorithms/theory/
```

## 12. Roli i Inteligjencës Artificiale në Zhvillim

Ky projekt është ndërtuar dhe përmirësuar me ndihmën e inteligjencës artificiale si asistencë zhvillimi. AI është përdorur për strukturimin e moduleve, organizimin e kodit, përmirësimin e ndërfaqes, formulimin e shpjegimeve akademike dhe optimizimin e integrimit me Tutor AI.

Megjithatë, vendimmarrja, përzgjedhja e funksionaliteteve dhe përshtatja me qëllimin akademik mbeten pjesë e punës zhvilluese të projektit.

## 13. Përfundim

LogicLab është një projekt ndërdisiplinor që lidh teorinë akademike me implementimin praktik. Ai demonstron se si Matematika Diskrete dhe Logjika Digjitale mund të përkthehen në një aplikacion web funksional, ndërsa Algoritmet dhe Programimi i Avancuar shpjegojnë koston e proceseve llogaritëse.

Përmes Tutor AI dhe analizës së imazheve, projekti zgjeron rolin e tij nga një analizues statik në një platformë interaktive mësimore. Arkitektura modulare e bën projektin të zgjerueshëm për funksionalitete të ardhshme si renderim grafik i qarqeve, eksportim raportesh, llogari përdoruesish dhe testim automatik.

Në aspekt profesional, LogicLab demonstron përdorimin e Django-s, strukturimin modular të kodit, integrimin me biblioteka simbolike, menaxhimin e të dhënave dhe përdorimin e AI lokale në një aplikacion akademik real.
