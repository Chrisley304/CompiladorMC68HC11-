*** VARIABLES ***
   
V1   EQU   $1032
PRUEBA   EQU   $1033
ADR4   EQU   $1034
OPTION EQU   $1039

*** PRINCIPAL ***
    JMP     BANDERA *DEBE DAR ERROR Error 1 o 2 o 3, No existe BANDERA
    BNE     BANDERA *DEBE DAR ERROR Error 3, No existe BANDERA

    ORG    $8000
INICIO
    ORG    $B123

    AB      *DEBE DAR ERROR Error 4, No existe mnemonico
    BNE     *DEBE DAR ERROR 5 carece de operando
    LDAA    *DEBE DAR ERROR 5 lo de arriba x2
    aba    $8000 *DEBE DAR ERROR 6 sobra de operando
    asr    $8000,y  *DEBE DAR ERROR 7 operando grande
    BNE     INICIO *DEBE DAR ERROR 8 salto lejano

JMP     SINBANDERA *DEBE DAR ERROR 9 Falta espacio relativo al margen

    JMP     SINBANDERA * Si debe jalar, pero es en post
    
    LDAA    $45
    LDAB    11
    BNE     INICIO
    LDAB    *DEBE DAR ERROR
    LDAA    #$80

SINBANDERA
    ldd     $17
    LDX     15  * NO se que hace
    ADDA    $7C
    ANDA    $F0
    ORG     $0123
    BNE     SINBANDERA
    JMP     INICIO

    *END     * Fin del programa *DEBE DAR ERROR 10 no se encuentra end
