   CPU "Z80.tbl"
   HOF "INT8"

   ORG 1000H

   LD A, 05; Carga el valor en la dirección de memoria 1001H en el registro A
   JR Z, eti1
   LD (0100H), A; Carga el valor de A en el registro B
   LD A, (1000H); Carga el valor en la dirección de memoria 1000H en el registro A
   LD D, B; Carga el valor de B en el registro D
   LD B, A ; Carga el valor de A en el registro C
eti2:; Etiqueta eti2
   JP eti2
   JP Z, eti1
   LD D, (IX + 05)
   LD HL, 1000H; Carga el valor de A en el registro D
   LD C, 03; Carga el valor de B en el registro C
eti3:; Etiqueta eti3
   LD A, B; Carga el valor 0 en el registro A
eti4:; Etiqueta eti4
   ADD A, 04; Suma el valor de D al registro A
   CP 00; Decrementa el valor de C
eti1:; Etiqueta eti1
   HALT; Detiene la CPU
   END
