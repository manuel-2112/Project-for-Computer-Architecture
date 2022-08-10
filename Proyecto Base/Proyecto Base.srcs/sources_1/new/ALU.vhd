library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ALU is
    Port ( a        : in  std_logic_vector (15 downto 0);   -- Primer operando.
           b        : in  std_logic_vector (15 downto 0);   -- Segundo operando.
           sop      : in  std_logic_vector (2 downto 0);   -- Selector de la operacion.
           c        : out std_logic;                       -- Senal de 'carry'.
           z        : out std_logic;                       -- Senal de 'zero'.
           n        : out std_logic;                       -- Senal de 'nagative'.
           result   : out std_logic_vector (15 downto 0));  -- Resultado de la operacion.
end ALU;

architecture Behavioral of ALU is

component Adder16
    Port(a  : in  std_logic_vector (15 downto 0);
         b  : in  std_logic_vector (15 downto 0);
         ci : in  std_logic;
         s  : out std_logic_vector (15 downto 0);
         co : out std_logic
         );
    end component;


signal alu_result   : std_logic_vector(15 downto 0);
signal add_result   : std_logic_vector(15 downto 0);
signal bMux         : std_logic_vector(15 downto 0);

signal co_add       : std_logic;
signal a_and_b      : std_logic_vector(15 downto 0);
signal a_or_b       : std_logic_vector(15 downto 0);
signal a_xor_b      : std_logic_vector(15 downto 0);
signal not_a        : std_logic_vector(15 downto 0);
signal shr_a        : std_logic_vector(15 downto 0);
signal shl_a        : std_logic_vector(15 downto 0);


begin

-- Operaciones

a_and_b <= a and b;
a_or_b <= a or b;
a_xor_b <= a xor b;
not_a <= not(a);
shr_a <= '0' & a(15 downto 1);
shl_a <= a(14 downto 0) & '0';

-- Mux
with sop(0) select
    bMux <= b      when '0',
            not(b) when '1';

inst_Add : Adder16 port map(
    a => a,
    b => bMux,
    ci => sop(0),
    s => add_result,
    co => co_add
    );
                
-- Resultado de la Operacion
               
with sop select
    alu_result <= add_result     when "000", --suma
                  add_result     when "001", --resta
                  a_and_b        when "010", --and
                  a_or_b         when "011", --or
                  a_xor_b        when "100", --xor
                  not_a          when "101", --not
                  shr_a          when "110", --shr
                  shl_a          when "111"; --shl
                  
result  <= alu_result;

-- Flags c z n

with sop select
    c <= co_add  when "000",
         co_add  when "001",
         a(0)   when "110",
         a(15)  when "111",
         '0'    when others;
        
with alu_result select
    z <= '1' when "0000000000000000",
         '0' when others;
         
--with alu_result(15) select --bit 15 no da la negatividad SI HAY RESTA Y NO HAY CARRY ES NEGATIVO
--    n <= '1' when '1',
--         '0' when others; --está malo

with sop select
    n <= not co_add when "001",
         '0'    when others;

end Behavioral;

