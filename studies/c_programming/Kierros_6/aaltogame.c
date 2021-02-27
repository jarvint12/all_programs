#include <stdio.h>
#include <stdlib.h>


namespace GameOfLifeApp
{
    class executeGameOfLife
    {
        static void Main(string[] args)
        {
            GameOfLifeApp app = new GameOfLifeApp();
            app.init_map();
            uint count = 0;
            while(Console.ReadKey().Key != ConsoleKey.Enter)
            {
                app.tic();
                count++;
                Console.WriteLine("Press enter to stop. This was {0} iteration",count);

            }
            Console.WriteLine("Maximum living cell cout {0}",app.getMaxLivingCells());
        }
    }
    class GameOfLifeApp{
        char[,] _map;
        uint _size = 0;
        uint _cellNumber = 0;
        uint _maxLivingCells = 0;

        public uint getMaxLivingCells(){
            return _maxLivingCells;
        }
        public void init_map(){
            Console.WriteLine("Give size of one side");

            while(!uint.TryParse(Console.ReadLine(),out _size))
            {
                Console.Write("That is not valid number\n");
            }

            _map = new char[_size,_size];

            for(uint x = 0; x < _size;x++)
            {
                for(uint y =0;y< _size;y++)
                {
                    _map[x,y] = 'X';
                }
            }
            add_cells();
            print_map();
        }

        void add_cells()
        {
            Console.WriteLine("Give starting number of cells");

            while(!uint.TryParse(Console.ReadLine(),out _cellNumber))
            {
                Console.Write("That is not valid number\n");
            }

            Console.WriteLine("I will randomize plazings because you're lazy.\n");
            _maxLivingCells = _cellNumber;
            for(uint i=0;i<_cellNumber;i++)
            {

                bool flag = true;
                while(flag){
                    Random rnd = new Random();

                    int x =  rnd.Next(0,(int) _size);
                    int y =  rnd.Next(0,(int) _size);
                    if(_map[x,y] == 'X')
                    {
                        _map[x,y] = 'O';
                        flag = false;
                    }

                }

            }
            Console.WriteLine("Placed cells.");


        }

        void print_map(){
            Console.WriteLine("Current map. ");
            for(uint i = 0;i<_size;i++){
                for(uint a = 0;a<_size;a++)
                {
                    Console.Write(_map[i,a]);
                }
                Console.Write('\n');
            }
            Console.Write('\n');
        }

        public void tic(){
            char[,] mapCpy = _map;
            print_map();
            uint sum =0;
            for(int x = 0; x< _size;x++)
            {
                for(int y = 0;y<_size;y++)
                {
                    /*Here we do comparison for mapCpy and change things in _map */
                    /*Check all surrounding spaces */
                    /*This migth be better done in another function */
                    for(sbyte i = -1;i<2;i++)
                    {
                        for(sbyte a = -1;a<2;a++)
                        {
                            if(!(a==0 && i == 0) && check_coordinate_validity(x+i,y+a))
                            {
                                if(mapCpy[x+i,y+a] == 'O')
                                {
                                    sum++;
                                }
                            }
                        }
                    }

                /*Apply changes */
                /*Migth be better style to do seperately */
                if(sum < 2 && mapCpy[x,y] == 'O')
                {
                    _map[x,y] = 'X';
                }

else if(sum > 3 && mapCpy[x,y] == 'O')
                {
                    _map[x,y] = 'X';
                }
                else if(sum == 3 && mapCpy[x,y] == 'X')
                {
                    _map[x,y] = 'O';
                }
                sum = 0;
                }
            }


        uint currentCellCount = countCells();
        if(currentCellCount > _maxLivingCells)
        {
            _maxLivingCells = currentCellCount;
        }
            print_map();
        }

        bool check_coordinate_validity(int x,int y){
            return !(x >= _size || y >= _size || x < 0 || y < 0);
        }
        uint countCells()
        {
            uint ret = 0;
            for(uint x = 0;x <_size;x++)
            {
                for(uint y =0;y<_size;y++)
                {
                    if(_map[x,y] == 'O')
                    {
                        ret++;
                    }
                }
            }
            return ret;
        }
    }
}
