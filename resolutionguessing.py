#!/usr/bin/env python3
import re

from screencalc import Resolution

def _guess_diag_from_string(s, verbose=False):
    
    # e.g.
    # 24" -> 24
    # 40' -> 40
    diag_guesses_symbol = re.findall(r'\d+["\']', s)
    if diag_guesses_symbol:
        diag_guess = diag_guesses_symbol[0]
        diag = int(re.findall(r'\d+', diag_guess)[0])
        if verbose:
            print("Guessing that >{}< means {} inches diagonal".format(
                diag_guess, diag))
        return diag
    
    # e.g.
    # 30 inch -> 30
    # 30  inches -> 30
    diag_guesses_inch = re.findall(r'\d+[\.\d+]*? inch', s)
    if diag_guesses_inch:
        diag_guess_inch = diag_guesses_inch[0]
        diag = float(re.findall(r'\d+[\.\d+]*', diag_guess_inch)[0])
        if verbose:
            print("Guessing that >{}< means {} inches diagonal".format(
                diag_guess_inch, diag))
        
        return diag

def _guess_size_from_string(s, verbose=False):
    size = None
    return size

def _guess_resolution_from_string(s, verbose=False):
    res_guesses = re.findall(r'\d{3,}[x\*]\d{3,}', s)
    if res_guesses:
        res_guess = res_guesses[0]
        
        res_list = re.findall(r'\d{3,}', res_guess)
        if res_list and len(res_list) >= 2:
            x_res, y_res = map(int, res_list[:2])
            if verbose:
                print("Guessing that >{}< means resolution {}x{}".format(
                    res_guess, x_res, y_res))
            return x_res, y_res
        else:
            if verbose:
                print("Problem guessing what >{}< means!".format(res_guess))
            return None, None

    x_res, y_res = None, None
    if re.findall(r'4k', s):
        x_res, y_res = (3840, 2160)
    
    if re.findall(r'1080p', s):
        x_res, y_res = (1920, 1080)
    
    if re.findall(r'1200p', s):
        x_res, y_res = (1920, 1200)
        
    if verbose and x_res and y_res:
        print("Guessing that >{}< includes resolution={}x{}".format(
            s, x_res, y_res))

    return x_res, y_res

def guess_resolution_from_string(string, verbose=False):
    """Takes a string and tries to generate a Resolution from it.
    Example of strings that work:
    '24" 1920x1080'
    '24" 1920*1080'
    '24 inch 4k'
    
    If verbose is True, print intermediate steps
    """
    x_res, y_res = _guess_resolution_from_string(string, verbose)
    diag = _guess_diag_from_string(string, verbose)
    size = _guess_size_from_string(string, verbose)
    
    if verbose:
        descr_list = []
        if x_res and y_res:
            descr_list.append("res={}x{}".format(x_res, y_res))
        if diag is not None:
            descr_list.append("diag={}".format(diag))
        if size is not None:
            descr_list.append("size={}".format(size))
            
        print("Creating resolution using {} from string '{}'".format(
            ", ".join(descr_list), string))
    resolution = Resolution(x_res, y_res, diag, size)
    return resolution

#Shortcuts
g = guess_resolution_from_string

def prompt():
    return guess_resolution_from_string(input("? "))

p = prompt
