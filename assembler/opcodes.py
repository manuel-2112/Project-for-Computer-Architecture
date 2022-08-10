OPCODES = {
"MOV_A_B" :"00000000000000000000",
"MOV_B_A": "00000000000000000001",
"MOV_A_LIT": "00000000000000000010",
"MOV_B_LIT": "00000000000000000011",
"MOV_A_DIR": "00000000000000000100",
"MOV_B_DIR": "00000000000000000101",
"MOV_DIR_A": "00000000000000000110",
"MOV_DIR_B": "00000000000000000111",
"ADD_A_B":"00000000000000001000",
"ADD_B_A":"00000000000000001001",
"ADD_A_LIT":"00000000000000001010",
"ADD_A_DIR":"00000000000000001011",
"ADD_DIR":"00000000000000001100",
"SUB_A_B":"00000000000000001101",
"SUB_B_A":"00000000000000001110",
"SUB_A_LIT":"00000000000000001111",
"SUB_A_DIR":"00000000000000010000",
"SUB_DIR": "00000000000000010001",
"AND_A_B": "00000000000000010010",
"AND_B_A": "00000000000000010011",
"AND_A_LIT": "00000000000000010100",
"AND_A_DIR":"00000000000000010101",
"AND_DIR":"00000000000000010110",
"OR_A_B":"00000000000000010111",
"OR_B_A":"00000000000000011000",
"OR_A_LIT":"00000000000000011001",
"OR_A_DIR":"00000000000000011010",
"OR_DIR": "00000000000000011011",
"XOR_A_B": "00000000000000011100",
"XOR_B_A": "00000000000000011101",
"XOR_A_LIT": "00000000000000011110",
"XOR_A_DIR": "00000000000000011111",
"XOR_DIR": "00000000000000101000",
"NOT_A":"00000000000000101001",
"NOT_B_A":"00000000000000101010",
"NOT_DIR_A":"00000000000000101011",
"SHL_A":"00000000000000101100",
"SHL_B_A":"00000000000000101101",
"SHL_DIR_A":"00000000000000101110",
"SHR_A":"00000000000000101111",
"SHR_B_A":"00000000000000110000",
"SHR_DIR_A":"00000000000000110001",
"INC_A":"00000000000000110010",
"INC_B":"00000000000000110011",
"INC_DIR":"00000000000000110100",
"DEC_A":"00000000000000110101",
"CMP_A_B":"00000000000000110110",
"CMP_A_LIT":"00000000000000110111",
"CMP_A_DIR":"00000000000000111000",
"JMP":"00000000000000111001",
"JEQ":"00000000000000111010",
"JNE":"00000000000000111011",
"MOV_A_(B)":"00000000000000111100",
"MOV_B_(B)":"00000000000000111101",
"MOV_(B)_A":"00000000000000111110",
"MOV_(B)_LIT":"00000000000000111111",
"ADD_A_(B)":"00000000000001000000",
"ADD_B_(B)":"00000000000001000001",
"SUB_A_(B)":"00000000000001000010",
"SUB_B_(B)":"00000000000001000011",
"AND_A_(B)":"00000000000001000100",
"AND_B_(B)":"00000000000001000101",
"OR_A_(B)":"00000000000001000110",
"OR_B_(B)":"00000000000001000111",
"XOR_A_(B)":"00000000000001001000",
"XOR_B_(B)":"00000000000001001001",
"NOT_(B)_A":"00000000000001001010",
"SHL_(B)_A":"00000000000001001011",
"SHR_(B)_A":"00000000000001001100",
"INC_(B)":"00000000000001001101",
"CMP_A_(B)":"00000000000001001110",
"JGT":"00000000000001001111",
"JGE":"00000000000001010000",
"JLT":"00000000000001010001",
"JLE":"00000000000001010010",
"JCR":"00000000000001010011",
"PUSH_A":"00000000000001010100",
"PUSH_B":"00000000000001010101",
"POP_A":"00000000000001010110",
"POP_A2":"00000000000001010111",
"POP_B":"00000000000001011000",
"POP_B2":"00000000000001011001",
"CALL":"00000000000001011010",
"RET":"00000000000001011011",
"RET_2": "00000000000001011100",
"ADD_B_LIT":"00000000000001011101",
"ADD_B_DIR":"00000000000001011110",
"SUB_B_LIT":"00000000000001011111",
"SUB_B_DIR":"00000000000001100000",
"AND_B_LIT":"00000000000001100001",
"AND_B_DIR":"00000000000001100010",
"OR_B_LIT":"00000000000001100011",
"OR_B_DIR":"00000000000001100100",
"XOR_B_LIT":"00000000000001100101",
"XOR_B_DIR":"00000000000001100110",
}