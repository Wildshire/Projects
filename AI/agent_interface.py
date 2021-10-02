from othello import OthelloState


class AgentInterface:
    """
    The interface of an Agent class

    This class defines the required methods that an agent class should
    implement.
    """
    @staticmethod
    def info():
        """
        Return the agent's information

        This function returns the agent's information as a dictionary variable.
        The returned dictionary should contain at least the `agent name`.

        Returns
        -------
        Dict[str, str]
        """
        raise NotImplementedError

    def decide(self, state: OthelloState, actions: list):
        """
        Generate a sequence of increasing good actions form `actions` list

        This is a generator function; it means it should have no return
        statement, but it should yield a sequence of increasing good actions.

        Parameters
        ----------
        state: OthelloState
            Current state of the board
        actions: list
            List of all possible actions

        Yields
        ------
        action
            the chosen `action` from the `actions` list
        """

        raise NotImplementedError

