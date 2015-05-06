# vuurschepen-northsea

Een simpele monte-carlo simulatie om twee polair-diagrammen van de Griel te vergelijken op basis van de gemiddelde windcondities in de maand mei over de route van de vuurschepen- en north-sea-race. Het verschil wordt uitgedrukt in gemiddelde seconden per uur, waar positieve waarden betekenen dat met code0 sneller is. 

De simulatie is met de volgende aannames geschreven:
- De polair diagrammen zijn bi-lineair
- Windrichting is gebaseerd op http://www.windfinder.com/windstatistics/p11-b
- Windsnelheid is normaal verdeeld met mean 15 en std 8.55 (dit geeft een P(x<=11) van 0.32
- Windrichting en snelheid zijn ongecorreleerd
- Windrichting en snelheid veranderen elk uur en leg
- De route die wordt gevaren is de rumpline (up en downwind wordt berekend mbv vmg)
- Stroom wordt niet meegerekend
