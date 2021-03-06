
from octopus.api.graph import Graph, CFGGraph
from octopus.platforms.NEO.disassembler import NeoDisassembler
from octopus.platforms.NEO.cfg import NeoCFG
from octopus.platforms.NEO.cfg import (enumerate_basicblocks_statically,
                                       enumerate_edges_statically,
                                       enumerate_functions_statically,
                                       assign_basicblocks_to_functions)

import unittest


class NeoCfgTestCase(unittest.TestCase):

    # lock contract
    bytecode_hex = "56c56b6c766b00527ac46c766b51527ac46c766b52527ac4616168184e656f2e426c6f636b636861696e2e4765744865696768746168184e656f2e426c6f636b636861696e2e4765744865616465726c766b53527ac46c766b00c36c766b53c36168174e656f2e4865616465722e47657454696d657374616d70a06c766b54527ac46c766b54c3640e00006c766b55527ac4621a006c766b51c36c766b52c3617cac6c766b55527ac46203006c766b55c3616c7566"
    disasm = NeoDisassembler(bytecode_hex)
    instructions = disasm.disassemble()

    bb = enumerate_basicblocks_statically(instructions)
    func = enumerate_functions_statically(instructions)
    func = assign_basicblocks_to_functions(bb, func)
    edges = enumerate_edges_statically(bb)

    cfg = NeoCFG(bytecode_hex)
    cfg2 = NeoCFG(instructions=instructions)

    # visualization
    # graph = CFGGraph(cfg)
    # graph.view()

    number_func = 1
    number_inst = 101
    number_basicblock = 4

    def testReverseInstructions(self):

        self.assertEqual(len(self.instructions), self.number_inst)

    def testEnumerateFunctions(self):

        self.assertEqual(len(self.func), self.number_func)
        self.assertEqual(len(self.func), len(self.cfg.functions))
        self.assertEqual(len(self.cfg.functions), len(self.cfg2.functions))

    def testEnumerateBasicBlocks(self):

        self.assertEqual(len(self.bb), self.number_basicblock)
        self.assertEqual(len(self.bb), len(self.cfg.basicblocks))
        self.assertEqual(len(self.cfg.basicblocks), len(self.cfg2.basicblocks))

    def testAssignBasicBlocksFunctions(self):
        # verify if every basicblock have been assign to a function
        all_bb = [func.basicblocks for func in self.cfg.functions]
        all_bb = sum(all_bb, [])
        self.assertEqual(len(all_bb), self.number_basicblock)
        self.assertEqual(len(all_bb), len(self.cfg.basicblocks))


class NeoCfgTestCaseMedium(NeoCfgTestCase):

    bytecode_hex = "0x5fc56b6c766b00527ac46c766b51527ac4610b4f7065726174696f6e3a206c766b00c37e61680f4e656f2e52756e74696d652e4c6f67616c766b00c30a43616c63756c61746f72876c766b52527ac46c766b52c3648300616c766b51c300c352c576006c766b51c351c3c476516c766b51c352c3c4617c6729e30f18a594e03b49bd70b4f62603cb5b4769476c766b53527ac452c576001143616c63756c61746f7220526573756c74c476516c766b53c3c46168124e656f2e52756e74696d652e4e6f74696679616c766b00c36c766b54527ac46254036c766b00c307426f6f6c65616e876c766b55527ac46c766b55c3646100616c766b51c300c36c766b56527ac452c576001a4f7065726174696f6e3a20426f6f6c65616e2056616c75653a20c476516c766b56c3c46168124e656f2e52756e74696d652e4e6f74696679616c766b51c300c36c766b54527ac462d9026c766b00c307496e7465676572876c766b57527ac46c766b57c3649100611470726f63657373696e6720496e74656765723a206c766b51c300c37e61680f4e656f2e52756e74696d652e4c6f67616c766b51c300c36c766b58527ac452c576001a4f7065726174696f6e3a20496e74656765722056616c75653a20c476516c766b58c3c46168124e656f2e52756e74696d652e4e6f74696679616c766b51c300c36c766b54527ac4622e026c766b00c309427974654172726179876316006c766b00c3095369676e617475726587620400516c766b59527ac46c766b59c3646800610b70726f63657373696e67206c766b00c37e61680f4e656f2e52756e74696d652e4c6f676152c576006c766b00c3c476516c766b51c300c361653302c46168124e656f2e52756e74696d652e4e6f74696679616c766b51c300c36c766b54527ac46293016c766b00c30748617368313630876327006c766b00c30748617368323536876316006c766b00c3095075626c69634b657987620400516c766b5a527ac46c766b5ac3643f006152c576006c766b00c3c476516c766b51c300c3c46168124e656f2e52756e74696d652e4e6f74696679616c766b51c300c36c766b54527ac46212016c766b00c3054172726179876c766b5b527ac46c766b5bc364bd00616c766b51c300c36c766b5c527ac452c576006c766b00c3c476516c766b5cc3c0c46168124e656f2e52756e74696d652e4e6f7469667961006c766b5d527ac4624f006153c576000a4172726179204974656dc476516c766b5dc3c476526c766b5cc36c766b5dc3c3c46168124e656f2e52756e74696d652e4e6f7469667961616c766b5dc351936c766b5d527ac46c766b5dc36c766b5cc3c09f6c766b5e527ac46c766b5ec3639cff6c766b5cc3c06c766b54527ac4623d0015556e68616e646c6564206f7065726174696f6e3a206c766b00c37e61680f4e656f2e52756e74696d652e4c6f6761006c766b54527ac46203006c766b54c3616c756652c56b6c766b00527ac46c766b51527ac453c56b6c766b00527ac4616c766b00c36c766b51527ac46c766b51c36c766b52527ac46203006c766b52c3616c756653c56b6c766b00527ac461516c766b00c36a527a527ac46c766b51c36c766b52527ac46203006c766b52c3616c756655c56b6c766b00527ac461006c766b51527ac4006c766b52527ac4622c00616c766b51c36c766b00c36c766b52c3517f7e6c766b51527ac4616c766b52c351936c766b52527ac46c766b52c36c766b00c3c09f6c766b53527ac46c766b53c363bfff6c766b51c36c766b54527ac46203006c766b54c3616c7566"

    disasm = NeoDisassembler(bytecode_hex)
    instructions = disasm.disassemble()

    bb = enumerate_basicblocks_statically(instructions)
    func = enumerate_functions_statically(instructions)
    func = assign_basicblocks_to_functions(bb, func)
    edges = enumerate_edges_statically(bb)

    cfg = NeoCFG(bytecode_hex)
    cfg2 = NeoCFG(instructions=instructions)

    # graph = CFGGraph(cfg)
    # graph.view_functions()
    # graph.view_functions(simplify=True)

    number_func = 4
    number_inst = 825
    number_basicblock = 33

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(NeoCfgTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(NeoCfgTestCaseMedium)
    unittest.TextTestRunner(verbosity=2).run(suite)
