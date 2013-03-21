#!/usr/bin/python

import argparse
import commands

class Evlt():

    SINGLE_SPACE = " "
    VLT_COMMAND = "vlt --credentials admin:admin "
    BASE_URL = SINGLE_SPACE + "http://localhost:4502/crx/-/jcr:root/"
    HOME_URL_JCR_ROOT = "/Users/khafaji/MyProjects/LBI_PROJECTS/trunk/vaa-website/src/main/resources/jcr_root/"
    
    CHECKOUT_COMMAND = " checkout "
    COMMIT_COMMAND = " commit "
    STATUS_COMMAND = " status "
    UPDATE_COMMAND = " update "
    EMPTY_STRING = ""    

    def doCommit(self, namespace):                
        commandParts = ""
        
        if namespace.updateSources:            
            self.updateSources()

        if namespace.isForceOperation:
            commandParts += " --force "


        print commands.getoutput(self.isDebugMode(namespace) + self.VLT_COMMAND + self.COMMIT_COMMAND + commandParts)

    def updateSources(self):        
        print "Updating the locals sources"

    def doCheckout(self, namespace):        

        if hasattr(namespace, "uri") & len(namespace.uri) > 0:
            commands.getoutput(self.isDebugMode(namespace) + self.VLT_COMMAND + self.CHECKOUT_COMMAND + self.BASE_URL + namespace.uri)
            print 'Checkout completed successfully'

    def doStatus(self, namespace):
        print commands.getoutput(self.isDebugMode(namespace) + self.VLT_COMMAND + self.STATUS_COMMAND)

    def doUpdate(self, namespace):
        print commands.getoutput(self.isDebugMode(namespace) + self.VLT_COMMAND + self.UPDATE_COMMAND)


    def __init__(self, *args):
        namespaceObject = self.defineCommandLineOptions()
        namespaceObject.func(namespaceObject)    

    def createCommitParser(self, subparsers):
        commitParser = subparsers.add_parser("commit", help="Send changes from your working copy to the repository.")
        
        commitParser.add_argument("-u", "--update-sources", dest="updateSources", action="store_true", help="Update the local copy of the CQ component sources")        
        commitParser.add_argument("-f", "--force", dest = "isForceOperation" , action="store_true", help="force checkout to overwrite local files if they already exist.")
        commitParser.add_argument("-q", "--quite", dest = "isQuiteOperation", action="store_true", help="Generate as little output as possible")
        
        commitParser.set_defaults(func=self.doCommit)        

    def createCheckoutCommand(self, subparsers):
        checkoutParser = subparsers.add_parser("checkout", help="Checkout a Vault file system")
        checkoutParser.add_argument("uri", action="store")
        checkoutParser.set_defaults(func=self.doCheckout)

    def createStatusParser(self, subparsers):
        statusParser = subparsers.add_parser("status", help="Display a report of the changed files")        
        statusParser.set_defaults(func=self.doStatus)

    def createUpdateParser(self, subparsers):
        updateParsers = subparsers.add_parser("update", help="Bring changes from the repository into the working copy.")
        updateParsers.set_defaults(func=self.doUpdate)

    def isDebugMode(self, namespace):
        if namespace.isDebugMode:
            return "echo "
        return self.EMPTY_STRING

    def defineCommandLineOptions(self):

        self.argumentParser = argparse.ArgumentParser(prog='vlt')
        self.argumentParser.add_argument("--debug", action="store_true", dest="isDebugMode")
        subparsers = self.argumentParser.add_subparsers()

        # Create a parser for the checkout command
        self.createCheckoutCommand(subparsers)

        # Create a parser for the commit command
        self.createCommitParser(subparsers)

        # Create a parser to the status command
        self.createStatusParser(subparsers)

        # Create a parser for the update command
        self.createUpdateParser(subparsers)

        # Create a parser for the
        
        return self.argumentParser.parse_args()

if __name__ == '__main__':
    Evlt()