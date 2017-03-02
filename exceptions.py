'''
Created on Feb 26, 2017

@author: mike thornton
@change: 
@copyright: 2017
'''

def doesNothing(arg1, keywd="mike"):
    '''
    doesNothing() has as default argument value.
    '''
    if keywd == "mike":
        return "Author"
    return 1



if __name__ == '__main__':
    
    x = 0x41
    y = int(x)
    z = chr(x)
    try:
        addThese = y + z
    except ZeroDivisionError:
        print "won't see this"
    except TypeError:
        print "a type error occured"
    finally:
        print y, " + ", z, " , won't work."
        
        
    #raise TypeError("myFavoriteMistake")


    print doesNothing(1,"mikes")
    print doesNothing.__doc__

        