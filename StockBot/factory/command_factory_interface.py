from .command_factory_xtb import CommandFactoryXTB
from .command_factory_abstract import CommandFactory

COMMAND_FACTORY = {
    "abstract": CommandFactory,
    "xtb":      CommandFactoryXTB
}