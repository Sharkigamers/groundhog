##
## EPITECH PROJECT, 2019
## minishell1
## File description:
## Makefile
##

all:	default

default:
	cp groundhog.py groundhog

clean:
	rm -f groundhog

fclean: clean

re:	fclean all

.PHONY: all clean fclean re
