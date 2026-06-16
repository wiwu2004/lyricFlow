
import requests

def carregar_lrc(caminho):
    linhas = []

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip() and linha.startswith("["):
                try:
                    tempo_txt = linha.split("]")[0][1:]
                    letra = linha.split("]")[1].strip()
                    if not letra:
                        continue
                    minutos, segundos = tempo_txt.split(":")
                    tempo = float(minutos) * 60 + float(segundos)
                    linhas.append((tempo, letra))
                except:
                    continue

    return linhas


def calcular_estado(linhas, indice_atual, tempo_atual):
    if indice_atual >= len(linhas):
        return indice_atual, "", "", ""

    tempo_linha, texto = linhas[indice_atual]

    if indice_atual + 1 < len(linhas):
        tempo_proxima = linhas[indice_atual + 1][0]
    else:
        tempo_proxima = tempo_linha + 3

    duracao = tempo_proxima - tempo_linha
    if duracao <= 0:
        duracao = 1

    progresso = (tempo_atual - tempo_linha) / duracao
    progresso = max(0, min(1, progresso))

    qtd = int(progresso * len(texto))

    parte_passada = texto[:qtd]
    parte_futura = texto[qtd:]

    proxima = ""
    if indice_atual + 1 < len(linhas):
        proxima = linhas[indice_atual + 1][1]

    return indice_atual, parte_passada, parte_futura, proxima


def buscar_lrc_api(artista, musica):
    url = f"https://lrclib.net/api/get?artist_name={artista}&track_name={musica}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Erro ao buscar lyrics")
            return []

        data = response.json()

        if "syncedLyrics" not in data or not data["syncedLyrics"]:
            print("Não tem lyrics sincronizada")
            return []

        lrc_texto = data["syncedLyrics"]

        return parse_lrc_text(lrc_texto)

    except Exception as e:
        print("Erro:", e)
        return []

def parse_lrc_text(lrc_text):
    linhas = []

    for linha in lrc_text.split("\n"):
        linha = linha.strip()
        if not linha.startswith("["):
            continue
        try:
            partes = linha.split("]", 1)
            if len(partes) < 2:
                continue
            tempo_txt = partes[0][1:]
            texto = partes[1].strip()
            if not texto:
                continue
            minutos, segundos = tempo_txt.split(":")
            tempo = float(minutos) * 60 + float(segundos)
            linhas.append((tempo, texto))
        except:
            continue

    return linhas
