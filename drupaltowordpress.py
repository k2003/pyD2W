#!/usr/bin/python
import sys, getopt
from database_interface import Database
from prettytable import PrettyTable


def print_diagnostics(diagnostic_results):
    drupal_posts = diagnostic_results["posts"]
    drupal_terms = diagnostic_results["terms"]
    drupal_duplicate_terms = diagnostic_results["duplicate_terms"]
    drupal_node_types = diagnostic_results["node_types"]
    drupal_terms_exceeded_charlength = diagnostic_results["terms_exceeded_charlength"]
    drupal_dupliate_alias = diagnostic_results["dupliate_alias"]
        
    print "\n=================================================="
    print "Starting Drupal To WordPress diagnostics"
    print "==================================================\n"
    
    # Print Properties Table
    table_properties = PrettyTable(["Property", "Found in Drupal"])
    table_properties.align["Property"] = "l"
    table_properties.align["Found in Drupal"] = "l"
    table_properties.add_row(["Terms", "There are {} terms".format(len(drupal_terms))] )
    table_properties.add_row( ["Node types", "There are {} node types".format(len(drupal_node_types))] )
    table_properties.add_row( ["Post entries", "There are {} post entries".format(len(drupal_posts))] )
    table_properties.add_row( ["Duplicate terms", "There are {} duplicate terms".format(len(drupal_duplicate_terms))] )    
    table_properties.add_row( ["Term character length exceeded", "{} terms exceed WordPress' 200 character length".format(len(drupal_terms_exceeded_charlength))] )
    table_properties.add_row( ["Duplicate aliases", "{} duplicate aliases found".format(len(drupal_dupliate_alias))] )    
    print table_properties
    
    # Print Node Types Table
    types_list = list(types["type"] for types in drupal_node_types)
    types_string = ", ".join(types_list)
    
    table_node_types = PrettyTable(["Node type"])
    table_node_types.align["Node type"] = "l"
    for row in drupal_node_types:
        table_node_types.add_row([row["type"]])
    
    print table_node_types


def run_diagnostics():
    database = Database("127.0.0.1","anthonylv","6F7bmXbnDeBctvKLqz8R","teia_d6" )
    
    # General analysis of Drupal database properties
    drupal_posts = database.get_drupal_posts()
    drupal_terms = database.get_drupal_terms()
    drupal_node_types = database.get_drupal_node_types()
    
    # Look for common problms    
    drupal_duplicate_terms = database.get_drupal_duplicate_terms()
    drupal_terms_exceeded_charlength = database.get_terms_exceeded_charlength()
    drupal_dupliate_alias = database.get_dupliate_alias()
    
    results = {
        "posts": drupal_posts,
        "terms": drupal_posts,
        "duplicate_terms": drupal_duplicate_terms,
        "node_types": drupal_node_types,
        "terms_exceeded_charlength": drupal_terms_exceeded_charlength,
        "dupliate_alias": drupal_dupliate_alias
    }
    print_diagnostics(results)
    

def run_fix():
    print "This process will alter your database"
    answer = query_yes_no("Are you sure you want to continue?", "no")
    if answer:
        print "You answered yes"
    else:
        print "You answered no"
    

def print_usage():
    print """\
Usage: drupaltowordpress.py [option] ... [-d diagnostic | -f fix | -h help]
Options:
-d diagnostic     : Run diagnostic
-f fix            : Try to fix database problems
-h help           : Hostname to connect to
"""    

#
# Recepie from http://code.activestate.com/recipes/577058/
#
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def main(argv):
    try:
      opts, args = getopt.getopt(argv,"dfh",["fix", "help", "diagnostic"])
    except getopt.GetoptError:
      print_usage()
      sys.exit(2)
      
    if len(opts) == 0:
        print_usage()
    else:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print_usage()
                sys.exit()
            elif opt in ("-d", "--diagnostic"):
                run_diagnostics()
            elif opt in ("-f", "--fix"):
                run_fix()
            
                
    
if __name__ == "__main__":
   main(sys.argv[1:])