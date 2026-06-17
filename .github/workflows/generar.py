import requests

# Agregá aquí las listas públicas que quieras combinar
FUENTES = [
    "https://iptv-org.github.io/iptv/index.m3u",
]

playlist = "#EXTM3U\n\n"
vistos = set()

for fuente in FUENTES:
    try:
        r = requests.get(fuente, timeout=30)
        r.raise_for_status()

        lineas = r.text.splitlines()

        i = 0
        while i < len(lineas):
            linea = lineas[i]

            if linea.startswith("#EXTINF") and i + 1 < len(lineas):
                url = lineas[i + 1].strip()

                if url not in vistos:
                    vistos.add(url)
                    playlist += linea + "\n"
                    playlist += url + "\n"

                i += 2
            else:
                i += 1

    except Exception:
        print(f"No se pudo leer {fuente}")

# Agregar canales propios
try:
    with open("mis_canales.m3u", encoding="utf-8") as f:
        lineas = f.read().splitlines()

    i = 0
    while i < len(lineas):
        linea = lineas[i]

        if linea.startswith("#EXTINF") and i + 1 < len(lineas):
            url = lineas[i + 1].strip()

            if url not in vistos:
                vistos.add(url)
                playlist += linea + "\n"
                playlist += url + "\n"

            i += 2
        else:
            i += 1

except FileNotFoundError:
    pass

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(playlist)
