#!/usr/bin/python3

import difflib
import sys, getopt

def file_diff(fil1, fil2):
  print("-----------------------------------")
  print("Comparing files")
  print(" > " + filenavn1)
  print(" < " + filenavn2)
  print("> = remote\n< = preferred")
  print("-----------------------------------")
  file1 = open(fil1).readlines()
  file2 = open(fil2).readlines()
  delta = difflib.unified_diff(file1, file2)
  return sys.stdout.writelines(delta)

def only_changed(filenavn1, filenavn2):

  # Open file for reading in text mode (default mode)
  f1 = open(filenavn1, "r")
  f2 = open(filenavn2, "r")

  # Print confirmation
  print("-----------------------------------")
  print("Comparing files")
  print("> = remote\n< = preferred")
  print(">+ = added to remote\n<+ = removed from remote")
  print("> " + filenavn1)
  print("< " + filenavn2)
  print("-----------------------------------")

  # Read the first line from the files
  file1_linje = f1.readline()
  file2_linje = f2.readline()

  # Initialize counter for line number
  linje_nummer = 1

  # Loop if either file1 or file2 has not reached EOF
  while file1_linje != '' or file2_linje != '':

      # Strip the leading whitespaces
      file1_linje = file1_linje.rstrip()
      file2_linje = file2_linje.rstrip()

      # Compare the lines from both file
      if file1_linje != file2_linje:

          # If a line does not exist on file2 then mark the output with + sign
          if file2_linje == '' and file1_linje != '':
              print(">+", "linje %d" % linje_nummer, file1_linje)
          # otherwise output the line on file1 and mark it with > sign
          elif file1_linje != '':
              print(">", "linje %d" % linje_nummer, file1_linje)
          # If a line does not exist on file1 then mark the output with + sign
          if file1_linje == '' and file2_linje != '':
              print("<+", "linje %d" % linje_nummer, file2_linje)
          # otherwise output the line on file2 and mark it with < sign
          elif file2_linje != '':
              print("<", "linje %d" %  linje_nummer, file2_linje)

          # Print a blank line
          print()

      #Read the next line from the file
      file1_linje = f1.readline()
      file2_linje = f2.readline()


      #Increment line counter
      linje_nummer += 1

  # Close the files
  f1.close()
  f2.close()


def main(argv):
   inputfile = ''
   outputfile = ''

   opts, args = getopt.getopt(argv,"i:o:")

   for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   only_changed(inputfile, outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])