from bd import *
from scrapper import *


# # [RS] Compara peliculas de una lista en una lista dada

def inicioCompararListas( idOriginList , idEndList ):
    
    # input idOriginList: ID de la lista que se quiere comparar || ej: "ls096276650"
    
    #       idEndList: ID unica o arreglo con los que se quiere comparar || 
    
    #       ej (1) "ls021428038" 
    
    #       ej (2) [ "ls021428038", "ls094566741" ]
    
    print("\n **********************************************************")
    
    print("\n Comenzando proceso de comparación")
    
    originTitles = obtenerTituloDeLista( idOriginList )
    
    
    result = []
    
    numIterator = 1
    
    if isinstance( idEndList , list ):                
        
        numIterator = len( idEndList ) 
        
        for i in range( numIterator ):
            
            auxMatrix = compararDosListas( originTitles, idEndList[ i ] )            
                    
            result.append( auxMatrix )
            
    else:
         
            auxMatrix = compararDosListas( originTitles, idEndList )            
                    
            result.append( auxMatrix )
    
    print("\n Fin de proceso de comparación ")
    
    print("\n **********************************************************")
    
    return result

def compararDosListas( originTitles, endTitle):
    
    # input originTitles: Lista que tiene todos los titulos de una lista || ej:  ( (12196, 'ls096276650', 'tt5503686'), (12197, 'ls096276650', 'tt8722346') )
    
    #       idEndList: ID unica o arreglo con los que se quiere comparar ||      ej  "ls021428038" 
    
    #TODO: RECIBE EL NOMBRE DE LAS LISTAS
    #BUSCA EL ID DE TODAS LAS PELICULAS DE LA LISTA DE ORIGEN Y CONSULTA SI EXISTE
    #PELICULAS ASOCIADAS EN BD
    result = []
    
    totalTitlesFounds = 0
    
    #result.insert( 0, totalTitlesFounds )
    
    for oTitle in originTitles: 
            
        if validarPeliculaEnLista( endTitle  , oTitle ):                    

            #result.append( 1 )
            print("oTitle: ", oTitle)

            totalTitlesFounds += 1

        #else:
            
                    # result.append( 0 )
                
    result.append( totalTitlesFounds ) 
    
    print( "\n Número de titulos contenidos en la lista: ", totalTitlesFounds)
    
    print(" \n Arreglo -> ", result )
    
    return result

def modelo( sPrima, L,):
    
    # S -> Num de peliculas de S
    
    # sub -> numero de peliculas de S'
    
    # n -> numero de peliculas que se encuentran en L
    
    # L -> numero de peliculas de L
    startMetadataListProcess(sPrima)
    startMetadataListProcess(L)

    sumSPrima = totalTittlesEnLista(sPrima)
    sumL = totalTittlesEnLista(L)
    numSPrimaEnL = compararDosListas( sPrima,L )
    S = sumSPrima*2
    prob= (S*numSPrimaEnL)/(sumSPrima*sumL)
    
    print("\n Resultado del modelo: ", prob)
