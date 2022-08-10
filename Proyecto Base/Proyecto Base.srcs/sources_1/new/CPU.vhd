library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_unsigned.all;
use IEEE.numeric_std.all;


entity CPU is
    Port (
           clock : in STD_LOGIC;
           clear : in STD_LOGIC;
           ram_address : out STD_LOGIC_VECTOR (11 downto 0);
           ram_datain : out STD_LOGIC_VECTOR (15 downto 0);
           ram_dataout : in STD_LOGIC_VECTOR (15 downto 0);
           ram_write : out STD_LOGIC;
           rom_address : out STD_LOGIC_VECTOR (11 downto 0);
           rom_dataout : in STD_LOGIC_VECTOR (35 downto 0);
           dis : out STD_LOGIC_VECTOR (15 downto 0));
end CPU;

architecture Behavioral of CPU is

-- Declaraci?n REG
component Reg
    Port (
        clock       : in    std_logic;
        clear       : in    std_logic;
        load        : in    std_logic;
        up          : in    std_logic;
        down        : in    std_logic;
        datain      : in    std_logic_vector (15 downto 0);
        dataout     : out   std_logic_vector (15 downto 0)
          );
    end component;

-- Declaraci?n ALU
component ALU
    Port (
           a        : in  std_logic_vector (15 downto 0);   -- Primer operando.
           b        : in  std_logic_vector (15 downto 0);   -- Segundo operando.
           sop      : in  std_logic_vector (2 downto 0);   -- Selector de la operacion.
           c        : out std_logic;                       -- Senal de 'carry'.
           z        : out std_logic;                       -- Senal de 'zero'.
           n        : out std_logic;                       -- Senal de 'nagative'.
           result   : out std_logic_vector (15 downto 0)   -- Resultado de la operacion.
           );  
    end component;

-- declaracion PC
component PC 
    Port ( 
        clock   :   in  std_logic;
        clear   :   in  std_logic;
        load    :   in  std_logic;
        up       : in  std_logic;
        down     : in  std_logic;
        datain  :   in  std_logic_vector (11 downto 0);
        dataout :   out std_logic_vector (11 downto 0));
    end component;

component SP 
    Port ( 
        clock   :   in  std_logic;
        clear   :   in  std_logic;
        load    :   in  std_logic;
        up       : in  std_logic;
        down     : in  std_logic;
        datain  :   in  std_logic_vector (11 downto 0);
        dataout :   out std_logic_vector (11 downto 0));
    end component;

-- Declaraci?n Registro Status


component ControlUnit is
    Port(
        opcode : in std_logic_vector(19 downto 0);
        Z: in std_logic;
        N: in std_logic;
        C: in std_logic;
        enableA: out std_logic;
        enableB: out std_logic;
        selA: out std_logic_vector(1 downto 0);
        selB: out std_logic_vector(1 downto 0);
        loadPC: out std_logic;
        sop: out std_logic_vector(2 downto 0);
        w: out std_logic;
        selAdd: out std_logic_vector(1 downto 0);
        incSP: out std_logic;
        decSP: out std_logic;
        selPC: out std_logic;
        selDin: out std_logic
        );
    end component;

component RegistroStatus is
    Port ( 
        clock   :  in  std_logic;
        clear   :  in  std_logic;
        c       :   in  std_logic;
        z       :   in  std_logic;
        n       :   in  std_logic;
        s       :   out std_logic_vector (2 downto 0)
        );
    end component;

component Adder12 is
    Port ( 
        a        : in  std_logic_vector (11 downto 0);
        b        : in  std_logic_vector (11 downto 0);
        result  : out std_logic_vector (15 downto 0)
    );
end component;


signal A   :   std_logic_vector(15 downto 0);
signal B   :   std_logic_vector(15 downto 0);

signal loadPC       : std_logic;
signal enableA      : std_logic;
signal enableB      : std_logic;

signal c_ALU_Status : std_logic;   
signal z_ALU_Status : std_logic;   
signal n_ALU_Status : std_logic;

signal selAdd : std_logic_vector(1 downto 0);   
signal incSP : std_logic;   
signal decSP : std_logic;
signal selPC : std_logic;   
signal selDin : std_logic;   

signal selA         : std_logic_vector(1 downto 0);
signal selB         : std_logic_vector(1 downto 0);
signal sop          : std_logic_vector(2 downto 0);
signal s            : std_logic_vector(2 downto 0);
signal result       : std_logic_vector(15 downto 0);
signal result12       : std_logic_vector(15 downto 0);

signal outSP       : std_logic_vector(11 downto 0);

signal muxAout  :   std_logic_vector(15 downto 0);
signal muxBout  :   std_logic_vector(15 downto 0);

signal muxPCout      : std_logic_vector(11 downto 0);
signal muxDinout       : std_logic_vector(15 downto 0);
signal muxSout       : std_logic_vector(11 downto 0);


signal rd : STD_LOGIC_VECTOR (11 downto 0);
signal test_a : STD_LOGIC_VECTOR (11 downto 0);

begin

rom_address <= test_a;
--dis(15 downto 8) <= A(7 downto 0);
--dis(7 downto 0) <= B(7 downto 0);
ram_address <= muxSout;
ram_datain <= muxDinout;
-- E1: ram_address <= rom_dataout(31 downto 20);
-- E1: ram_datain <= result;

-- Mux A
with selA select
    muxAout <= A                       when "00",
               "0000000000000000"      when "01",
               "0000000000000001"      when "10",
               "0000000000000000"      when "11";

-- Mux B
with selB select
    muxBout <= B                         when "00",
               "0000000000000000"        when "01",
               rom_dataout(35 downto 20) when "10",
               ram_dataout               when "11";
-- Mux PC
with selPC select
    muxPCout <= ram_dataout(11 downto 0)  when '0', --DOUT
                rom_dataout(31 downto 20) when '1'; --LIT

-- MUX Din
with selDin select
    muxDinout <= result12    when '0', --PC
                 result      when '1'; --ALU

-- MUX S
with selAdd select
    muxSout <=  rom_dataout(31 downto 20) when "00", --LIT
                B(11 downto 0)            when "01", --B
                outSP                     when "10", --SP
                "000000000000"            when "11"; --??


inst_PC: PC port map(
    clock       => clock,
    clear       => clear,
    load       => loadPC,
    up       => '1',
    down     => '0',
    datain => muxPCout, --12 del literal
    -- E1: datain => rom_dataout(31 downto 20),
    dataout  => test_a
    );

inst_ControlUnit: ControlUnit port map(
    opcode => rom_dataout(19 downto 0),
    Z => s(1),
    N => s(0),
    C => s(2),
    enableA => enableA,
    enableB => enableB,
    selA => selA,
    selB => selB,
    loadPC => loadPC,
    sop => sop,
    w => ram_write,
    selAdd => selAdd,
    incSP => incSP,
    decSP => decSP,
    selPC => selPC,
    selDin => selDin
    );

inst_RegA: Reg port map(
    clock       => clock,
    clear       => clear,
    load        => enableA,
    up          => '0',
    down        => '0',
    datain      => result,
    dataout     => A --MUXA
    );

inst_RegB: Reg port map(
    clock       => clock,
    clear       => clear,
    load        => enableB,
    up          => '0',
    down        => '0',
    datain      => result,
    dataout     => B --MUXB
    );

inst_ALU: ALU port map(
    a        => muxAout, --MUX RESULT
    b        => muxBout, --MUX RESULT
    sop      => sop,
    c        => c_ALU_Status,
    z        => z_ALU_Status,
    n        => n_ALU_Status,
    result   => result
    );

inst_Status: RegistroStatus port map(
    clock   => clock,
    clear   => clear,
    c       => c_ALU_Status,
    z       => z_ALU_Status,
    n       => n_ALU_Status,
    s       => s
    );

inst_SP: SP port map(   --CONECTAR
        clock   =>   clock,
        clear   =>   clear,
        load    =>   '0',
        up      => incSP,
        down    => decSP, 
        datain  =>   "111111111111", --NO SIRVE DE NADA
        dataout =>   outSP
    );

inst_Adder12: Adder12 port map( --CONECTAR
        a        => "000000000001",
        b        => test_a,
        result   => result12
    );

end Behavioral;
