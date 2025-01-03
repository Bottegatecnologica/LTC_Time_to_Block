import requests
from datetime import datetime, timezone
import time


def get_block_ltc(date_time_str):
    """
    Calcola il numero di blocco Litecoin (LTC) dato un input di data e ora.
    Usa il formato 'YYYY-MM-DD HH:MM:SS' per la data e ora.
    """
    try:
        # Debug: stampa l'input ricevuto
        print(f"[DEBUG] Data e ora ricevuta: {date_time_str}")

        # Converti la data e ora in un timestamp Unix
        dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        target_timestamp = int(dt.timestamp())

        # Debug: stampa il timestamp Unix calcolato
        print(f"[DEBUG] Timestamp Unix target: {target_timestamp}")

        # Ottieni il blocco corrente
        url_block_count = "https://chainz.cryptoid.info/ltc/api.dws?q=getblockcount"
        current_block = int(requests.get(url_block_count).text)

        # Debug: stampa il numero del blocco corrente
        print(f"[DEBUG] Blocco corrente: {current_block}")

        # Ottieni il timestamp del blocco corrente
        url_block_time = f"https://chainz.cryptoid.info/ltc/api.dws?q=getblocktime&height={current_block}"
        current_timestamp = int(requests.get(url_block_time).text)

        # Debug: stampa il timestamp del blocco corrente
        print(f"[DEBUG] Timestamp del blocco corrente: {current_timestamp}")

        # Verifica che il timestamp target sia valido
        if target_timestamp > current_timestamp:
            return "Errore: la data fornita è nel futuro. Fornire una data valida."

        # Tempo medio tra i blocchi (2.5 minuti)
        avg_block_time = 150

        # Stima iniziale del blocco di partenza
        estimated_block = current_block - (current_timestamp - target_timestamp) // avg_block_time

        # Debug: stampa la stima iniziale del blocco
        print(f"[DEBUG] Stima iniziale del blocco: {estimated_block}")

        # Limiti di ricerca binaria
        low = 0
        high = current_block
        closest_block = None

        while low <= high:
            mid = (low + high) // 2
            url_block_time = f"https://chainz.cryptoid.info/ltc/api.dws?q=getblocktime&height={mid}"

            # Debug: stampa il blocco che si sta esaminando
            print(f"[DEBUG] Verificando il blocco: {mid}")

            try:
                mid_timestamp = int(requests.get(url_block_time).text)
            except requests.exceptions.RequestException as e:
                return f"Errore durante la connessione all'API: {e}"
            except ValueError:
                return "Errore nel parsing del timestamp del blocco."

            # Debug: stampa il timestamp del blocco intermedio
            print(f"[DEBUG] Timestamp del blocco {mid}: {mid_timestamp}")

            if mid_timestamp < target_timestamp:
                low = mid + 1
                closest_block = mid
            elif mid_timestamp > target_timestamp:
                high = mid - 1
            else:
                print(f"[DEBUG] Blocco trovato: {mid}")
                return mid  # Trovato il blocco esatto

            time.sleep(1)  # Rispetta il limite delle API (1 richiesta ogni 10 secondi)

        # Debug: stampa il blocco più vicino trovato
        print(f"[DEBUG] Blocco più vicino trovato: {closest_block}")
        return closest_block

    except Exception as e:
        print(f"Errore: {e}")


# Esempio di utilizzo
if __name__ == "__main__":
    data_e_ora = input("Inserisci la data e ora (formato 'YYYY-MM-DD HH:MM:SS'): ")
    risultato = get_block_ltc(data_e_ora)
    print(f"Il numero del blocco Litecoin corrispondente è: {risultato}")
