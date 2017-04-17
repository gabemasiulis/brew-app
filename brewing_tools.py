import xml.etree.ElementTree as ET

# NOTE - This class may not be functional as is. It needs dev work and testing.
class BrewTimer(object):
    """ a collection of timer controls for a brewing system."""
    def __init__(self, mn=0, sec=0):
        self.mn = mn
        self.sec = sec
        self.resetMn = mn
        self.resetSec = sec


    def Set(self, mn=0, sec=0):
        """ setting the timer, values are ints """
        # we make sure to only set the timer with integers
        assert type(mn) == int and type(sec) == int,\
               'Set() must be called with type int!'
        self.mn = mn
        self.sec = sec
        # storing values away for reseting the timer
        self.resetMn = mn
        self.resetSec = sec

    def Run(self):
        """ the actual count down, values are ints"""
        if self.sec == 0:
            self.mn -= 1
            self.sec = 59

        else:
            self.sec -= 1


    def Reset(self):
        """ Resets the timer to previous self.Set value. """
        self.Set(self.resetMn, self.resetSec)

    def GetDisplay(self):
        """
        Returns a dict of int mn, int sec, string 'mn:sec'
        """
        display = '{:02d}:{:02d}'.format(self.mn, self.sec)

        return display


class BeerXMLParser(object):
    ''' A class for parsing a beer xml file.'''
    def __init__(self):
        # initializing some variables
        self.recipe_name = ''
        self.boil_time = ''
        self.brew_type = ''

        self.mash_steps = []
        self.first_wort = []
        self.boil_hops = {}
        self.dry_hop = []
        self.all_steps = {}


    def set_XML(self, fp):
        ''' Sets up the root of a specified xml document and calls
        functions to get some data. Call with the full file path to
        a beer.xml doucment
        '''
        self.tree = ET.parse(fp)
        # the <RECIPE> element of the tree contains all of the data we want
        self.recipe = self.tree.getroot()[0]
        self.recipe_name = self.recipe.find('NAME').text
        self.boil_time = self.recipe.find('BOIL_TIME').text.split('.')[0]
        self.brew_type = self.recipe.find('TYPE').text

        ### I think EST is what we need here?!!! ###
        # self.volume = self.recipe.find('BATCH_SIZE').text
        # self.og = self.recipe.find('EST_OG').text
        # self.abv = self.recipe.find('EST_ABV').text

        self.set_mash_steps()
        self.set_hops()


    def set_mash_steps(self):
        ''' Returns a tuple of (name, time, temperature) for each
        mash step into a list. All values are collected as strings.
        '''
        # other ineresting mash setp elements that could be useful:
        # TYPE, INFUSE_AMOUNT, DECOCTION_AMOUNT, INFUSE_TEMP

        # reset any old values
        self.mash_steps = []
        # loop through the tee and find our mash steps
        for step in self.tree.iter('MASH_STEP'):
            name = step.find('NAME').text
            # dropping the trailing 0's
            time = step.find('STEP_TIME').text.split('.')[0]
            farenheit = round(float(step.find('STEP_TEMP').text) * 1.8 + 32)
            temp = "{:.0f}".format(farenheit)
            elements = (name, time, temp)
            self.mash_steps.append(elements)


    def set_hops(self):
        ''' Returns a dict of all the hops for the recipe.
        Boil hops are collected in a dict with boil time in seconds (int) as the key
        and a tuple of (name, amt, time, use) (strings) for the value.
        Dry hops and first wort hops are collected in lists.
        '''
        # reset any old values
        self.first_wort = []
        self.boil_hops = {}
        self.dry_hop = []

        for hop in self.tree.iter('HOP'):
            name =  hop.find('NAME').text
            # convert the weight from mg to oz
            amt ="{:.2f}".format(float(hop.find('AMOUNT').text) * 35.274)
            # dropping the trailing 0's
            time = hop.find('TIME').text.split('.')[0]
            time_in_seconds = int(time) * 60
            use = hop.find('USE').text

            hop_data = (name, amt, time, use)

            if use == 'First Wort':
                self.first_wort.append(hop_data)

            elif use == 'Dry Hop':
                self.dry_hop.append(hop_data)

            elif time_in_seconds not in self.boil_hops:
                self.boil_hops[time_in_seconds] = [hop_data]

            else:
                self.boil_hops[time_in_seconds].append(hop_data)


    def get_mash_steps(self):
        ''' returns a list of mash steps '''
        return self.mash_steps


    def get_boil_hops(self):
        ''' returns the dict of boil hops '''
        return self.boil_hops


    def get_first_wort(self):
        ''' returns the list of first wort hops '''
        return self.first_wort


    def get_dry_hops(self):
        ''' returns the list of dry hops '''
        return self.dry_hop


    def get_all_steps(self):
        ''' Returns a dict of all brew day mand and boil
        steps and the associated values as strings.
        '''
        self.all_steps = {'mash':self.mash_steps, 'first_wort':self.first_wort,
                          'boil':self.boil_hops, 'dry_hop':self.dry_hop}

        return self.all_steps


    def get_recipe_name(self):
        ''' returns the name of the recipe as a string '''
        return self.recipe_name


    def get_boil_time(self):
        ''' returns the length of the boil in minutes as a string '''
        return self.boil_time


    def get_brew_type(self):
        ''' returns the type of brew, (all grain, extract, etc.) as a string '''
        return self.brew_type




# tests
if __name__ == '__main__':
    fpath = 'C:/Users/Todd/Desktop/brewweb/recipes/Oktober-16.xml'
    xml = BeerXMLParser()
    xml.set_XML(fpath)
    mash = xml.get_mash_steps()
    boilh = xml.get_boil_hops()
    fw = xml.get_first_wort()
    dh = xml.get_dry_hops()
    get_all = xml.get_all_steps()
    recipe = xml.get_recipe_name()
    boilt = xml.get_boil_time()
    btype =  xml.get_brew_type()

    #print mash
    #print boilh
    #print fw
    #print dh
    #print get_all
    #print recipe
    #print boilt
    #print btype
    #get_all['recipe_name'] = recipe
    print get_all
