Költségkövető – Python / Tkinter

Hallgató: Barta Simon (BS)
Tantárgy: Szkript nyelvek
Projekt: Költségkövető mini alkalmazás

Rövid leírás:
A program egy egyszerű költségkövető alkalmazás, amelyben a felhasználó rögzítheti a mindennapi kiadásait, valamint kereshet és összesítést készíthet belőlük. Az adatok egy CSV fájlban kerülnek mentésre, így a program újraindítás után is visszatölti a korábbi tételeket. A felület Tkinterrel készült, modern, sötét témájú elrendezéssel.

Fő funkciók:
- Új költségtételek rögzítése (dátum, kategória, összeg, megjegyzés)
- Tételek megjelenítése táblázatos formában
- Adatok mentése és betöltése CSV fájlból
- Szabad szöveges keresés
- Szűrés törlése
- Tétel törlése
- Összes kiadás számítása
- Napi és havi összesítés

Fájlok és modulok:

main.py:
A grafikus felület és a program indítása.
Fontosabb metódusok:
- load_from_file
- refresh_list
- update_total
- apply_search
- clear_search
- add_expense
- delete_selected
- calculate_summary
Belépési pont: if __name__ == "__main__": main()

expenses_bs.py:
Külön modul a költségtételek kezelésére.
- ExpenseBS osztály: date, category, amount, description
- osszeg_bs: összegzés
- save_expenses_to_csv_bs: mentés CSV-be
- load_expenses_from_csv_bs: betöltés CSV-ből

Használt könyvtárak:
- tkinter
- csv
- os

Használat:
1. Python 3 szükséges.
2. Program indítása: python main.py
3. Az adatok automatikusan betöltődnek az expenses_bs.csv fájlból.
4. Új tétel hozzáadásához ki kell tölteni a mezőket és a Hozzáadás gombra kattintani.
5. Keresés: keresőmező + Szűrés gomb.
6. Törlés: kijelölt tétel törlése a Törlés gombbal.
7. Összesítés: napi vagy havi mód kiválasztása, majd dátum/hónap megadása.

CSV formátum:
date;category;amount;description
2025-11-24;Étel;3200;Gyros
