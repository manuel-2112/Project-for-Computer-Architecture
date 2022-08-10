library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity RegistroStatus is
    Port ( 
        clock   :  in  std_logic;
        clear   :  in  std_logic;
        c       :   in  std_logic;
        z       :   in  std_logic;
        n       :   in  std_logic;
        s       :   out std_logic_vector (2 downto 0)
        );
end RegistroStatus;

architecture Behavioral of RegistroStatus is

begin

reg_prosses : process (clock)                   -- Proceso sensible a clock
        begin
            if (clear = '1') then             -- Si clear = 1
                s <= (others => '0');         -- Carga 0 en el registro.
            elsif (rising_edge(clock)) then
                s <= c & z & n;
            end if;
        end process;
        
end Behavioral;
