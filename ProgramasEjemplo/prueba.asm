*** VARIABLES ***
   
V1   EQU   $1032
PRUEBA   EQU   $1033
ADR4   EQU   $1034
OPTION EQU   $1039

*** PRINCIPAL ***
    ORG    $8000
INICIO
    AB
    JMP     SINBANDERA
    LDAA    $45
    LDAB    11
    BNE     SINBANDERA
    LDAB    *DEBE DAR ERROR
    LDAA    #$80

SINBANDERA
    ldd     $17
    LDX     15  * NO se que hace
    ADDA    $7C
    ANDA    $F0
    BNE     SINBANDERA
    JMP     INICIO
    JMP     BANDERA *DEBE DAR ERROR

    END     * Fin del programa