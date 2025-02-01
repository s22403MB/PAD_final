# PAD_final - Aplikacja została wdrożona jako publiczna pod adresem https://pad-final.streamlit.app/

## W moim projekcie skupiam się na analizie zbioru danych z https://www.kaggle.com/datasets/sahistapatel96/bankadditionalfullcsv zawierającego ponad 40 tys. rekordów dot. telefonicznej reklamy bankowej, a dokładniej lokaty. 
## Moim celem będzie odnalezienie najoptymalniejszego modelu uczenia maszynowego, do zwiększenia zysków banku. W tym celu sprawdzę również najistotniejsze cechy jakie mają wpływ na ten proces.

# Struktura plików projektu składa się z:
1. Folderu data - przechowywane są w nim pliki pośrednie na etapie analizy. Plik źródłowy jest pobierany w kodzie bezpośrednio z kaggle przy użyciu *kagglehub*.
2. Folderu models - przechowywane są w nim modele wykorzystywane w pliku *demo.py* oraz podfolderu testing gdzie przechowywane są modele do pliku *models.py*.
3. analysis.py - punkt 4 wymagań - analiza danych. Zawiera wykresy. dot najważniejszych kolumn, tabele krzyżowe dla danych kategorycznych oraz interpretacje badań.
4. demo.py - plik pozwalający na przetestowanie formularza dot. danych ze zbioru i sprawdzenie czy marketing byłby w takim przypadku sukcesem.
5. first_analysis.ipynb - plik w którym została przeprowadzona wstępna analiza zbioru, zawiera szczegółowe opisy transformacji oraz preprocessingu. (Warto jednak zaznaczyć, że nie wszystkie jego elementy zostały przeniesione do rozwiązania końcowego). Plik sam nie stanowi części projektu, ale jest wkładem który pozwolił na utworzenie reszty.
6. import_data.py - punkt 2 wymagań - pozwala na łatwiejsze pobieranych danych z kaggle, ale również z dysku czy przy użyciu jobliba.
7. main.py - punkt 5 wymagań (ale składają się na niego również wszystkie podstrony), startowy plik streamlita - zawiera linki do podstron, oraz podstawowe ustawienia używane w całym projekcie.
8. models.py - punkt 6 wymagań - zawiera przetestowane modele uczenia maszynowego, ich metryki, model końcowy oraz krótki opis czemu akurat dany model został wybrany.
9. preprocessing.ipyngb - plik zawierający deklaracje transformera, pipelinenów, modeli końcowych. Uruchomienie go jest niezbędne by wygenerować pliki do folderu *data*. Jednak dla łatwości użycia, pliki zostały zaimprotowane również do githuba.
10. processing.py - punkt 3 wymagań - choć tak naprawdę preprocessing jest realizowany w pliku powyżej, opisuje on jakie operacje zostały wykonane (Ważne: niektóre przekształcenia zostały wykonane już na etapie pliku *analysis.py*).
11. raw_data.py - punkt 5 wymagań - plik strony głównej na streamlicie, zawiera on wykresy oraz opisy surowych danych, pozwala on na "wgryzienie się" w dane oraz na wyciągnięcie wstępnych wniosków niezbędnych do dalszej analizy.

Inne:
- requirements.txt - plik niezbędny do działania streamlita
- .gitignore - celem uniknięcia niepotrzebnych plików w repozytorium

Aby uruchomić rozwiązanie wystarczy skorzystać z linku powyżej, albo można uruchomić go na własnym komputerze zapewniając środowisko spełniające wymagania z pliku *requirements.xt* oraz pythona w wersji 3.11.7
Komenda do uruchomienia rozwiązania to *streamlit run main.py*
