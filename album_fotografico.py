from csv import reader, writer

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r") as csvfile:
            csvfile.readline() #skip della la prima riga
            csvfile = reader(csvfile) #creo oggetto reader dal modulo csv

            anni = [] #lista con tutti gli anni delle foto nel file csv
            album = [] #struttura dati dell'album fotografico

            for foto in csvfile: #scorro su tutte le foto del file
                codice_foto = foto[0] #salvo il codice identificativo della foto
                titolo_foto = foto[1]
                autore_foto = foto[2]
                mese_foto = int(foto[3])
                anno_foto = int(foto[4]) #salvo l'anno della foto

                dict_foto = dict() #creo un dizionario per la foto che analizzo
                dict_foto[codice_foto] = [titolo_foto, autore_foto, mese_foto, anno_foto] #riempio il dizionario

                if anno_foto not in anni: #verifico che l'anno della foto non sia stato già inserito nell'elenco degli anni
                    anni.append(anno_foto)

                    anno = dict() #dizionario che associa a ciascun anno una lista di foto - - - 2019: [foto1, foto2, foto3]
                    anno[anno_foto] = [] #lista di tutte le foto inizialmente vuota
                    album.append(anno) #aggiungo il dizionario "anno" alla struttura dati


                for dict_anno in album: #scorro i dizionari/anni dell'album
                    if anno_foto in dict_anno: #trovo il dizionario che ha come chiave l'anno della foto che sto analizzando
                        dict_anno[anno_foto].append(dict_foto) #aggiungo il dizionario della foto analizzata al dizionario dell'anno (quindi all'album)
                        break

        return album
    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    #verifica per il mese
    if mese > 12 or mese < 1:
        return False

    #verifica per il codice
    for dict_anno in album: #scorro gli anni
        for chiave_anno in dict_anno: #prendo la chiave
            for dict_foto in dict_anno[chiave_anno]: #scorro le foto
                if codice in dict_foto: #verifico che il codice sia nel dizionario della foto
                    return None

    #verifica per il file
    try:
          with open(file_path, "a") as csvfile:
            csvfile = writer(csvfile)
            csvfile.writerow([codice, titolo, autore, mese, anno]) #scrittura della riga
    except FileNotFoundError:
        return None

    dict_foto = dict()
    dict_foto[codice] = [titolo, autore, mese, anno]  # alla chiave "codice" associo tutti i dati della foto"

    presente = False
    for dict_anno in album:
        if anno in dict_anno: #in pratica controllo se esiste l'anno della nuova foto come chiave di un dizionario dell'album
            presente = True
            break               #se all'interno dell'album c'è già l'anno della foto, presente diventa TRUE

    if presente == False:  #se l'anno non è nell'album ## da qui devo estrapolare come aggiungere la foto anche se l'anno è già presente
        dict_anno = dict()  #creo il dizionario "anno"
        dict_anno[anno] = []

        dict_anno[anno].append(dict_foto)
        album.append(dict_anno)

    elif presente == True: #se invece l'anno c'è già
        for dict_anno in album:
            if anno in dict_anno:
                dict_anno[anno].append(dict_foto) #aggiungo la foto alla lista di foto di quell'anno
                break

    return dict_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
