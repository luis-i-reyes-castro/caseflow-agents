"""
State Machine Base Class
"""

from abc import ABC, abstractmethod
from transitions import ( Machine,
                          State)
from typing import Type

from .basemodels import Message


class StateMachineBase(ABC) :
    """
    Base class for chatbot state machines built with `transitions` \\
    Tracks the underlying Machine plus helper utilities for handlers.
    """
    
    def __init__( self, debug : bool = False) -> None :
        """
        Initialize the base machine container \\
        Args:
            debug : When True, derived machines may log additional details
        """
        
        self.debug   : bool          = debug
        self.machine : Type[Machine] = None
        self.state   : str           = None
        self.states  : list[State]   = None
        
        return
    
    def build_dummy_methods_for_on_enter_and_on_exit(self) -> None :
        """
        Ensure every on_enter/on_exit callback exists (fallback is a no-op) \\
        Logic: For each state's `on_enter` callback function (say `callback`): If `self.callback` does not exist then assign it a dummy function taking no arguments and returning nothing. Same for each state's 'on_exit' callback function.
        """
        for state in self.states :
            for on_enter_callback in state.on_enter :
                if not hasattr( self, on_enter_callback) :
                    setattr( self, on_enter_callback, lambda : None)
            for on_exit_callback in state.on_exit :
                if not hasattr( self, on_exit_callback) :
                    setattr( self, on_exit_callback, lambda : None)
        
        return
    
    def get_actions(self) -> set[str] :
        """
        Get names of `on_enter` callbacks at the current state \\
        Returns:
            Set of callback names
        """
        return set(self.machine.get_state(self.state).on_enter)
    
    @abstractmethod
    def ingest_message( self, message : Type[Message]) -> None :
        """
        Ingest a single message and fire corresponding triggers \\
        Args:
            message : Instance of a Message subclass
        """
        raise NotImplementedError
    
    def reset(self) -> None :
        """
        Reset the machine state and derived per-session attributes \\
        """
        
        if "idle" in ( state.name for state in self.states ) :
            self.state = "idle"
        
        for attr_name, attr_val in self.__dict__.items() :
            
            if ( "_choice" in attr_name ) and isinstance( attr_val, str) :
                self.__dict__[attr_name] = None
            
            if ( "_agent_context" in attr_name ) and isinstance( attr_val, list) :
                self.__dict__[attr_name].clear()
        
        return
