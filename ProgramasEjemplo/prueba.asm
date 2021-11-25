*** VARIABLES ***
   
V1   EQU   $1032
PRUEBA   EQU   $1033
ADR4   EQU   $1034
OPTION EQU   $1039

*** PRINCIPAL ***
    ORG    $8000

INICIO
    NOP
    JMP     SINBANDERA
    BNE     INICIO
    BNE     SINBANDERA
    BRCLR   $00,X,#$80 INICIO   
    BRCLR   $00,X,#$80 SINBANDERA
    NOP
    LDAA    $45
    LDAB    11
    LDAA    #$80

SINBANDERA
    ldd     $17
    LDX     15  
    ADDA    $7C
    ANDA    $F0
    BNE     SINBANDERA
    JMP     INICIO

    END   
