
#                   Copyright (c) 2021, Serum Studio

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import optparse
import inspect
from typing import Callable
from typing import Any
from typing import Optional
from typing import get_type_hints
from .utils import CommandDict
from .parser import HelpCommand, HypeParser


class HypeCLI:
    """
    
    """

    #: This variable is used for storing all commands.
    #: Return dictionary.
    __commands: dict = {}
    __parser = HypeParser()

    def __init__(self, *, help_command: Callable[..., Any] = None, banner: Optional[str] = None):


        #: Your custom help command for the app.
        #: Default value = None
        self.help = help_command or HelpCommand

        #: Set if you want to add banner for the app
        #: Default value = False
        self.__banner = banner

        #: Set some parser options/config
        self.help.banner = banner
        self.__parser.help_command = self.help
        


    @property
    def commands(self):
        """ List of all commands """
        return [item[0] for item in self.__commands.items()]

    @property
    def banner(self):
        """ The banner for the application """
        return self.__banner

    @banner.setter
    def banner(self, value):
        """ Set the value of the banner. """

        if value == "":
            raise ValueError("Banner cannot be none")

        self.__banner = value
        return self.__banner

    def command(self, name: Optional[str] = None, description: Optional[str] = None, 
            value: Optional[Any] = None, type: Optional[Any] = None, required: Optional[bool] = False,
            deprecated: Optional[bool] = False, _func: Callable[..., Any] = None):

        """
        A command decorator for creating commands.

        Example:

            >>> app = HyperCLI()
            >>> ...
            >>> @app.commands(name='greet')
            >>> def greet(name: str):
            >>>     print(f"Hello {name}!")


        Parameters:
            Here are some parameters for the decorator: @command.

            name (str):
                The name of the command. If none, return the function name

            description (str):
                The description for the command.
            
            value (str):
                Default value for the command.

            type (Any):
                Set the type of the value.

            required (bool):
                Set if the command is required.

            deprecated (bool):
                Set if the command is deprecated.
        
        """

        #: The name of the command.
        #: If none, the function name will be setted.
        _name = name or _func.__name__

        #: The description of the command.
        #: Default Value: None
        _desc = description

        #: The default value for the command
        #: Default Value: None
        _default = value

        self.__type = type

        #: Set if the command is hidden or no.
        #: Default value: False
        _required = required

        #: Set if the command is deprecated
        #: Defautl Value: False
        _deprecated = deprecated


        
        def deco(_func):
            
            #: Get the signature of the function
            #: In order to get the parameters.
            sign = inspect.signature(_func)

            #: Get the type hint of the parameter
            type_hints = get_type_hints(_func)

            #: All parameters stored here.
            #: TYPE: List of tuples (%param%, %annotation%)
            params = []
            
            for param in sign.parameters.values():
                
                if param.name in type_hints:
                    annotation = type_hints[param.name]
                    
                    if self.__type == None:
                        self.__type = annotation

                    _params = (param.name, annotation)

                else:
                    if self.__type != None:
                        _params = (param.name, self.__type)
                    else:
                        _params = (param.name, None)

                params.append(_params)


            #: A command dict for storing a dictionary of command.
            command_dict = CommandDict(name = _name, params = params, desc = _desc,
                    default = _default, type = self.__type, required = _required, deprecated = _deprecated, func = _func)

            #: Add the command to the dictionary of commands.
            self.__commands.update(command_dict.dict())

            return _func
                
        return deco(_func) if _func else deco


    def prompt(self, prompt: Optional[str] = None, # Question to be prompt to
                default: Optional[Any] = None, # The default answer for the prompt question
                type: Optional[Any] = None, # Type of the answer. Like for example: bool, str, int
                required: Optional[bool] = False # Set if the prompt is required.
        ):

        """
        A decorator for handling prompt/questions.
        
        Example:

            >>> app = HyperCLI()
            >>> ...
            >>> @app.prompt("Do you like hyper cli?", type=bool, required=True)
            >>> def prompt_example(response):
            >>> ...
            >>> ...
            >>> if __name__ == "__main__":
            >>>     app.run()


        Parameters:
            Here are some parameters for the decorator: @prompt.

            prompt (str):
                The question used to be prompt.
                Default value: None

            default (any):
                The default value for the prompted question. 
                Default value: Any

            type (any):
                You may define the type of the response.
                Default value: Any

            required (bool):
                Set if the question is required to answer.
                Default value: False

        """

        #: THe question used to be prompt.
        #: Default Value: None
        _prompt = prompt

        #: The default value for the question
        #: Default Value: None
        _default = default

        #: The type of the response
        #: Default Value: Any
        _type = type

        #: Set if the prompt is required or not.
        #: Default Value: False
        _required = required



    def run(self):
        """
        Run the application as well as load all the commands.
        
        Example Application:

            >>> app = HyperCLI()
            >>> ...
            >>> @app.commands(name='greet')
            >>> def greet(name: str):
            >>>     print(f"Hello {name}!")
            >>> ...
            >>> if __name__ == "__main__":
            >>>     app.run() 
        
        """
        for command in self.commands:

            self.__parser.add_argument(
                    command, 
                    self.__commands[command]['desc'], 
                    value=self.__commands[command]['default'], 
                    required=self.__commands[command]['required'], 
                    type=self.__commands[command]['type'], 
                    deprecated=self.__commands[command]['deprecated']
                )
            
            command_params = self.__commands[command]['params']
            
            if len(command_params) > 1:
                print("Function has 2 parameter")

            print(self.__commands[command])
            args = self.__parser.parse_args()
            self.__commands[command]['func'](args[command])
