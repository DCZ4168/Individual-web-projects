SELECT Linea AS Line, ROUND(AVG(CAST(NumCCReal AS int)),2) AS Max_line
FROM [202408] --For november use [202411]
WHERE TIPODIAMO = 'LA'
GROUP BY Linea
ORDER BY CAST(Linea AS int) ASC