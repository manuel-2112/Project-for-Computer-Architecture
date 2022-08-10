library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_unsigned.all;

entity SP is
    Port ( 
        clock    : in  std_logic;
        clear    : in  std_logic;
        load   : in  std_logic;
        up       : in  std_logic;
        down     : in  std_logic;
        datain   : in  std_logic_vector (11 downto 0);
        dataout  : out std_logic_vector (11 downto 0)
    );
end SP;

architecture Behavioral of SP is

signal reg : std_logic_vector(11 downto 0) := (others => '1'); --PREGUNTAR


begin

-- preguntar al profe por la lógica

reg_prosses : process (clock, clear)        -- Proceso sensible a clock y clear.
        begin
          if (clear = '1') then             -- Si clear = 1
            reg <= (others => '1');         -- Carga 0 en el registro.
          elsif (rising_edge(clock)) then   -- Si flanco de subida de clock.
            if (load = '1') then            -- Si clear = 0, load = 1.
                reg <= datain;              -- Carga la entrada de datos en el registro.
            elsif (up = '1') then           -- Si clear = 0,load = 0 y up = 1.
                reg <= reg + 1;             -- Incrementa el registro en 1.
            elsif (down = '1') then         -- Si clear = 0,load = 0, up = 0 y down = 1. 
                reg <= reg - 1;             -- Decrementa el registro en 1.          
            end if;
          end if;
        end process;
        
dataout <= reg; 

end Behavioral;
