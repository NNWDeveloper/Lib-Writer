=========================================================
             NNW Lib-Writer 1.0
=========================================================

Jednoduchý textový editor s podporou formátu ODT a PDF,
vytvořený v jazyce Python pomocí knihovny PySide6 (Qt6).

---------------------------------------------------------
OBSAH
---------------------------------------------------------
1. Popis aplikace
2. Funkce
3. Požadavky
4. Instalace a spuštění
5. Struktura projektu
6. Klávesové zkratky
7. Známé problémy
8. Autor a licence
---------------------------------------------------------


1) POPIS APLIKACE
---------------------------------------------------------
NNW Lib-Writer 1.0 je grafický textový editor, který umožňuje
práci s dokumenty ve formátu ODT (OpenDocument Text) a TXT.
Umožňuje formátování textu, vkládání obrázků a tabulek,
změnu písma i barvy a export dokumentu do PDF.

Program podporuje také automatické ukládání obsahu
každých 60 sekund do souboru "autosave.odt".

Je určen pro uživatele Linuxu a Windows.
Aplikaci lze spustit buď jako Python skript, nebo jako
samostatnou spustitelnou aplikaci přeloženou pomocí Nuitka.


2) HLAVNÍ FUNKCE
---------------------------------------------------------
- Otevření a uložení souborů (ODT, TXT)
- Automatické ukládání (autosave)
- Formátování textu (tučné, kurzíva, podtržené)
- Změna písma a barvy textu
- Zarovnání textu (vlevo, na střed, vpravo, do bloku)
- Vkládání obrázků a tabulek
- Export do PDF
- Přehledné grafické rozhraní


3) POŽADAVKY
---------------------------------------------------------
Pro spuštění Python verze aplikace:
  - Python 3.9 nebo novější
  - Nainstalované knihovny:
        pip install PySide6 odfpy

Pro spuštění přeložené (binární) verze na Linuxu:
  - Nainstalované systémové knihovny Qt/X11:
        sudo apt install libxcb-cursor0 libxkbcommon-x11-0 \
             libxcb-xinerama0 libxcb-render-util0 \
             libxcb-image0 libxcb-keysyms1


4) INSTALACE A SPUŠTĚNÍ
---------------------------------------------------------
VARIANTA A – Spuštění jako Python skript:
  1. Otevři terminál ve složce s projektem.
  2. Spusť příkaz:
        python3 main.py

VARIANTA B – Spuštění přeložené verze (Nuitka):
  1. Přelož aplikaci:
        python3 -m nuitka --standalone \
            --enable-plugin=pyside6 \
            --include-qt-plugins=platforms \
            --onefile main.py
  2. Spusť výsledný soubor:
        ./main


5) STRUKTURA PROJEKTU
---------------------------------------------------------
NNW Lib-Writer 1.0/
│
├── main.py              hlavní soubor aplikace
├── README.txt           tento soubor s dokumentací


6) KLÁVESOVÉ ZKRATKY
---------------------------------------------------------
Tučné písmo .............. Ctrl + B
Kurzíva .................. Ctrl + I
Podtržení ................ Ctrl + U
Otevřít soubor ........... Ctrl + O
Uložit soubor ............ Ctrl + S
Export do PDF ............ Ctrl + E
Změna písma .............. Ctrl + F
Změna barvy textu ........ Ctrl + K


7) ZNÁMÉ PROBLÉMY
---------------------------------------------------------
- Pokud se při spuštění zobrazí chyba:
    qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
  znamená to, že chybí knihovna "libxcb-cursor0".
  Řešení:
    sudo apt install libxcb-cursor0

- Ukládání ODT zatím podporuje pouze čistý text
  (bez obrázků a pokročilého formátování).


8) AUTOR A LICENCE
---------------------------------------------------------
Autor:  NNW (Nikita Novák / NNW Software)
Verze:  1.0
Rok:    2025
Kontakt: nnwsoft@example.com

Licence: MIT License
Tento projekt můžeš volně používat, upravovat i šířit,
pokud zachováš informaci o autorovi.

=========================================================
Děkujeme za používání NNW Lib-Writer 1.0
=========================================================
