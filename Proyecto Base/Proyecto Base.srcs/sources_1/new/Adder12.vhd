library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_unsigned.all;
use IEEE.numeric_std.all;

entity Adder12 is
    Port ( 
        a        : in  std_logic_vector (11 downto 0);
        b        : in  std_logic_vector (11 downto 0);
        result  : out std_logic_vector (15 downto 0)
    );
end Adder12;

architecture Behavioral of Adder12 is

begin

result <= ("0000" & b) + 1;



end Behavioral;
