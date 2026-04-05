# FireTV Fernbedienung

Eine browserbasierte Fernbedienung für Amazon FireTV Sticks. Ein Docker-Container verbindet sich per ADB (Android Debug Bridge) über das Netzwerk mit dem Stick und führt Tastenbefehle aus, die über eine Web-Oberfläche auf Port 5555 ausgelöst werden.

## Voraussetzungen

- Docker
- FireTV Stick im selben Netzwerk wie der Host-Rechner
- ADB-Debugging auf dem FireTV Stick aktiviert (siehe unten)

## ADB-Debugging auf dem FireTV Stick aktivieren

1. **Entwickleroptionen freischalten**
   - Einstellungen → Mein Fire TV → Info
   - Den Eintrag „Fire TV Stick" **7-mal hintereinander** antippen
   - Es erscheint die Meldung „Entwickleroptionen aktiviert"

2. **ADB-Debugging einschalten**
   - Einstellungen → Mein Fire TV → Entwickleroptionen
   - „ADB-Debugging" auf **Ein** stellen

3. **Netzwerk-Debugging einschalten**
   - In denselben Entwickleroptionen
   - „Netzwerk-ADB aktivieren" (oder „Apps aus unbekannten Quellen") auf **Ein** stellen

4. **IP-Adresse des Sticks herausfinden**
   - Einstellungen → Mein Fire TV → Info → Netzwerk
   - Die angezeigte IP-Adresse wird beim Start als `FIRETV_IP` übergeben

Beim ersten Verbindungsaufbau erscheint auf dem TV-Bildschirm ein Dialog „RSA-Schlüssel erlauben?" — diesen bestätigen.

## Starten

```bash
FIRETV_IP=192.168.1.x FIRETV_AUTH=meinpasswort ./start.sh
```

Die Web-Oberfläche ist danach erreichbar unter:

```
http://server:5555/?firetvauth=meinpasswort
```

Der Token wird beim ersten Aufruf aus der URL entfernt und in der Browser-Session gespeichert — er taucht also nicht dauerhaft im Verlauf auf. Ohne `FIRETV_AUTH` läuft der Server ohne Authentifizierung.

## Hilfsskripte

| Skript | Funktion |
|---|---|
| `./start.sh` | Image bauen und Container starten |
| `./build.sh` | Image neu bauen (ohne Container zu starten) |
| `./debug.sh` | Logs des laufenden Containers anzeigen |
