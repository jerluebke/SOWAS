# Poster
## Einleitung
Ziel des Versuches ist die Untersuchung der Ausbreitungsgeschwindigkeit v einer
Reihe von Dominosteinen.  
Konkret geht es um folgende Fragen:  
Wie hängt die v mit dem Abstand der Steine zusammen? Wie entwickelt sich v
mit der Zeit? Wie groß ist der Einfluss der Reibung?

## Theoretische Betrachtung
**TODO: Winkel und Maße aktualisieren**
![fig.1](dominoes.png)

Aus der Geometrie des Problems findet man eine Folge, welche die
Winkelgeschwindigkeit des vordersten Steins in Abhängigkeit in aller zuvor
gefallener Steine beschreibt. Diese Folge ist konvergent, d.h. nach diesem
Modell gibt es eine Grenzgeschwindigleit, an die sich v annährt.  
Nach etwas rechnen findet man:

![eq.1](v_as.png)

Wobei \dot{\theta} die Winkelgeschwindigkeit als Funktion von \theta im
Grenzfall ist.  
Die Berechnungen werden von einem Computerprogramm durchgeführt.

## Experimentelle Durchführung
Für die Messung werden die Steine in gleichem Abstand mit Schleifpapier als
Unterlage (zur Reibungsminimierung) aufgestellt, per Hand angestoßen (ein
qualitativer Vergleich verschiedener Anstoßgeschwindigkeiten genügt) und mit
einem Mikrofon aufgezeichnet. Aus der Tondatei lassen sich die zeitlichen
Abstände der Stöße entnehmen, womit dann v bestimmt werden kann. Diese Messung
wird für verschiedene Abstände wiederholt.  
Zum Vergleich wird noch eine Messreihe auf einer glatten Unterlage
durchgeführt.

**TODO: Nur eine Messreihe**
![fig.2](messung.png)

## Auswertung
**TODO: Beschriftung**
![fig.3](vergleich.png)

**TODO: gemessener Gleitreibungskoeffizient**

In dem Experiment stellt sich nach kurzer Zeit deutlich eine annährend
gleichbleibende Endgeschwindkigkeit ein(vgl. _fig.2_), welche als Mittelwert
mit Standardabweichung aus diesem fast konstanten Teil der gewonnen Daten
berechnet wird. In _fig.3_ sind diese Ergebnisse zusammen mit den theoretisch
errechneten Werten gegen den zugehörigen Abstand aufgetragen.  
Die Messung auf einer glatten Unterlage erweist sich als problematisch, da eine
Auswertung der Tondatei nur für große Abstände und nur mit recht großer
Streuung möglich ist, da die Steine aufgrund der viel geringeren Haftreibung
deutlich mehr Bewegungsfreiheit haben.

## Diskussion
Bei dem Vergleich von experimentellen und theoretischen Daten fällt eine gute
Korrelation für Abstände 2.0 cm >= \lambda >= 3.5 cm auf; für den oberen und
unteren Grenzfall weicht die Theorie etwas nach oben ab.

**TODO:**  
Theorie:
 - Annahme von Energieerhaltung der Wellenfront mit empirischem Korrekturfaktor  

Experiment:
 - schwierige Auswertung für kleine Abstände (Rauschen)  

allg.:
 - mögliches Zurückspringen der Steine
 - viele Unebenheiten bei Unterlage, Aufstellung, Position zueinander (wirkt
   sich alles für kleine Abstände stärker aus)  

mögliche Verbesserungen:
 - detailiertere Beachtung von Störfaktoren in der Theorie (Zurückspringen)
 - detailiertere Betrachtung der wirkenden (Scher-) Kräfte für eine genauere
   Beschreibung
 - Reduzierung von Unebenheiten im Aufbau, z.B. mit Schablone
 - genauere Messung mit besserem Mikrofon oder Highspeed-Kamera (ca. 1000 fps)

Fazit: einfache Mathematik der Mechanik <-> Komplexität der Anwendung
