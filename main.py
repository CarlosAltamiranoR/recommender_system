

#from numpy import *

from bd import *
from rs import *
from  scrapper import *



if __name__ == '__main__':



    # "https://www.imdb.com/list/ls096276650/?sort=alpha,asc&st_dt=&mode=detail&page=1"
    endList = []
    endList.append("ls033953605")#L1
    endList.append("ls023589784")#L2
   
    
    originList = "ls096276650" #lista del usuario u con peliculas que encuentra similares
 
    #startMetadataListProcess( "tt0111161", None )
    startMetadataListProcess( originList, endList )
    #modelo("ls023589784","ls033953605")


    
  

