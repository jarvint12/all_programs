/* monster.c -- Implementation of monster actions
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "dungeon.h"

// for defining some monster types below that can be used in the game
typedef struct {
    char name[20];  // Name of monster
    char sign;  // character to show it on map
    unsigned int hplow;  // lowest possible initial maxhp
    unsigned int hphigh;  // highest possible initial maxhp
} MonstType;

// Specifying three monster types to start with.
// Feel free to add more, or change the below
// Note that it is up to you to decide whether to use this array from createMonsters
// you may or may not use it
const MonstType types[] = {
    { "Goblin", 'G', 6, 10},
    { "Rat", 'R', 3, 5},
    { "Dragon", 'D', 15, 20}
};


/* One kind of attack done by monster.
 * The attack function pointer can refer to this.
 *
 * Parameters:
 * game: the game state
 * monst: The monster performing attack
 */
void attackPunch(Game *game, Creature *monst) {
    printf("%s punches you! ", monst->name);
    int hitprob = 50;
    int maxdam = 4;
    if (rand() % 100 < hitprob) {
        printf("Hit! ");
        int dam = rand() % maxdam + 1;
        printf("Damage: %d ", dam);
        game->hp = game->hp - dam;
        if (game->hp <= 0)
            printf("You died!");
        printf("\n");
    } else {
        printf("Miss!\n");
    }
}


/* Exercise (c)
 *
 * Move monster 'monst' towards the player character.
 * See exercise description for more detailed rules.
 */
void moveTowards(Game *game, Creature *monst) {
  int distance_x = game->position.x - monst->pos.x;
  int distance_y = game->position.y - monst->pos.y;

  if((abs(distance_x)+abs(distance_y))==1)  {
    return;
  }
  if(distance_y>0 && (isBlocked(game, monst->pos.x, (monst->pos.y+1))==0))  {
    monst->pos.y = monst->pos.y+1;
  }
  else if(distance_y<0 && (isBlocked(game, monst->pos.x, (monst->pos.y-1))==0))  {
    monst->pos.y = monst->pos.y-1;
  }
  else if(distance_x>0 && (isBlocked(game, (monst->pos.x+1), monst->pos.y)==0))  {
    monst->pos.x = monst->pos.x+1;
  }
  else if(distance_x<0 && (isBlocked(game, (monst->pos.x-1), monst->pos.y)==0))  {
    monst->pos.x = monst->pos.x-1;
  }
  else  {
    return;
  }
}

/* Exercise (d)
 *
 * Move monster 'monst' away from the player character.
 * See exercise description for more detailed rules.
 */
void moveAway(Game *game, Creature *monst) {
  int distance_x = game->position.x - monst->pos.x; //Mikäli >0, pelaajan x>monsterin x
  int distance_y = game->position.y - monst->pos.y; //Mikäli >0, pelaajan y>monsterin y

  if(distance_y>=0 && isBlocked(game, monst->pos.x, (monst->pos.y-1))==0)  { //Tarkistetaan monsterin seuraava kohta
    monst->pos.y = monst->pos.y-1; //Mikäli tarkistus meni läpi, siirretään monsteri yhden kauemmaksi
  }
  else if(distance_y<0 && (isBlocked(game, monst->pos.x, (monst->pos.y+1))==0))  {
    monst->pos.y = monst->pos.y+1;
  }
  else if(distance_x>=0 && (isBlocked(game, (monst->pos.x-1), monst->pos.y)==0))  {
    monst->pos.x = monst->pos.x-1;
  }
  else if(distance_x<0 && (isBlocked(game, (monst->pos.x+1), monst->pos.y)==0))  {
    monst->pos.x = monst->pos.x+1;
  }
  else  {
    return;
  }
}

/* Exercise (e)
 *
 * Take action on each monster (that is alive) in 'monsters' array.
 * Each monster either attacks or moves (or does nothing if no action is specified)
 */
void monsterAction(Game *game) {
    for (unsigned int i = 0; i < game->numMonsters; i++)  {

      if(game->monsters[i].hp<=0) {
        return;
      }

      int distance_x = game->position.x - game->monsters[i].pos.x;
      int distance_y = game->position.y - game->monsters[i].pos.y;
      if((abs(distance_x)+abs(distance_y))==1)  {
        game->monsters[i].attack(game, &game->monsters[i]);
      }

      else  {
        game->monsters[i].move(game, &game->monsters[i]);
      }
    }
    return;
}


/* Exercise (b)
 *
 * Create opts.numMonsters monsters and position them on valid position
 * in the the game map. The moster data (hitpoints, name, map sign) should be
 * set appropriately (see exercise instructions)
 */
void createMonsters(Game *game) {
    int i=0;
    int x = rand() % ((int)game->opts.mapWidth + 1 - 1) +1;
    int y = rand() % ((int)game->opts.mapHeight + 1 - 1) +1;
    int j=0;
    game->monsters = malloc(game->opts.numMonsters*sizeof(Creature));

    while(i<((int)game->opts.numMonsters))  {

      while((isBlocked(game, x, y))!=0)  {
        x= rand() % ((int)game->opts.mapWidth + 1 - 1) +1;
        y = rand() % ((int)game->opts.mapHeight + 1 - 1) +1;
      }
      game->monsters[i].pos.x = x;
      game->monsters[i].pos.y = y;

      j=rand() % (3 + 1 - 1) + 1;
      switch(j) {
    	case 1:
    		strcpy(game->monsters[i].name,"Goblin");
        game->monsters[i].sign = 'G';
        game->monsters[i].maxhp = 10;
        game->monsters[i].hp = (float)game->monsters[i].maxhp;
        game->monsters[i].attack = attackPunch;
        game->monsters[i].move = moveTowards;
    		break;
    	case 2:
    		strcpy(game->monsters[i].name, "Rat");
        game->monsters[i].sign = 'R';
        game->monsters[i].maxhp = 5;
        game->monsters[i].hp = (float)game->monsters[i].maxhp;
        game->monsters[i].attack = attackPunch;
        game->monsters[i].move = moveTowards;
    		break;
    	case 3:
    		strcpy(game->monsters[i].name, "Dragon");
        game->monsters[i].sign = 'D';
        game->monsters[i].maxhp = 20;
        game->monsters[i].hp = (float)game->monsters[i].maxhp;
        game->monsters[i].attack = attackPunch;
        game->monsters[i].move = moveTowards;
    		break;
    	}
      i++;
      game->numMonsters = i;
    }
}

/* Determine whether monster moves towards or away from player character.
 */
void checkIntent(Game *game)
{
    for (unsigned int i = 0; i < game->numMonsters; i++) {
        Creature *m = &game->monsters[i];
        if (m->hp <= 2) {
            m->move = moveAway;
        } else {
            m->move = moveTowards;
        }
        if (m->hp < m->maxhp)
            m->hp = m->hp + 0.1;  // heals a bit every turn
    }
}
