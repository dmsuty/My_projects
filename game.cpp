#include <bits/stdc++.h>
#define pb push_back
#define f first
#define s second

using namespace std;

struct player
{
    int id, h, s, f, b, x, y;
    char d;
};

player me;
int e, o;
vector < pair <int, int> > destroyed_platform;
vector < pair <int, int> > damaged_platform;
vector < vector < pair <int, int> > > rays;
vector < pair <int, int> > battery;
vector < pair <int, int> > food;
pair <int, int> targ_eat;
vector <player> enemies;
bool attack_platform = false;
bool attack_sword = false;
bool attack_ray = false;
bool failure = false;
bool finish = false;
bool death = false;
bool is_target = false;
const int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};
map <char, int> ctd = {{'N', 0}, {'E', 1}, {'S', 2}, {'W', 3}};

void read()
{
    cin >> me.id >> me.h >> me.s >> me.f >> me.b >> me.x >> me.y >> me.d;
    cin >> e >> o;
    for (int i = 0; i < e; ++i)
    {
        string s;
        cin >> s;
        int curr;
        if (s == "pickup_food")
        {
            int trash;
            cin >> trash;
        }
        if (s == "pickup_battery")
        {
            int trash;
            cin >> trash;
        }
        if (s == "attack")
        {
            cin >> curr;
            attack_sword = true;
        }
        if (s == "attack_ray")
        {
            cin >> curr;
            attack_ray = true;
        }
        if (s == "attack_platform")
        {
            attack_platform = true;
        }
        if (s == "death")
        {
            death = true;
        }
        if (s == "failure")
        {
            failure = true;
        }
        if (s == "finish")
        {
            finish = true;
        }
    }
    for (int i = 0; i < o; ++i)
    {
        string s;
        cin >> s;
        int player_curr;
        if (s == "ray")
        {
            int id, ray_n;
            cin >> id >> ray_n;
            vector < pair <int, int> > curr_ray;
            curr_ray.pb({id, 0});
            for (int i = 0; i < ray_n; ++i)
            {
                pair <int, int> hlp;
                cin >> hlp.f >> hlp.s;
                curr_ray.pb(hlp);
            }
            rays.pb(curr_ray);
        }
        if (s == "food")
        {
            int food_n;
            pair <int, int> curr_food;
            cin >> food_n;
            for (int i = 0; i < food_n; ++i)
            {
                cin >> curr_food.f >> curr_food.s;
                food.pb(curr_food);
            }
        }
        if (s == "battery")
        {
            int battery_n;
            pair <int, int> curr_battery;
            cin >> battery_n;
            for (int i = 0; i < battery_n; ++i)
            {
                cin >> curr_battery.f >> curr_battery.s;
                battery.pb(curr_battery);
            }
        }
        if (s == "damaged_platform")
        {
            int platform_n;
            pair <int, int> curr_platform;
            cin >> platform_n;
            for (int i = 0; i < platform_n; ++i)
            {
                cin >> curr_platform.f >> curr_platform.s;
                damaged_platform.pb(curr_platform);
            }
        }
        if (s == "destroyed_platform")
        {
            int platform_n;
            pair <int, int> curr_platform;
            cin >> platform_n;
            for (int i = 0; i < platform_n; ++i)
            {
                cin >> curr_platform.f >> curr_platform.s;
                destroyed_platform.pb(curr_platform);
            }
        }
        if (s == "player")
        {
            player curr_player;
            cin >> curr_player.x >> curr_player.y >> curr_player.d >> curr_player.id >> curr_player.h;
            int trash;
            cin >> trash;
            enemies.pb(curr_player);
        }
    }
}

void clean()
{
    destroyed_platform.clear();
    damaged_platform.clear();
    rays.clear();
    battery.clear();
    food.clear();
    enemies.clear();
    attack_platform = false;
    attack_sword = false;
    attack_ray = false;
    failure = false;
    finish = false;
    death = false;
}
void turn_r()
{
    if (me.d == 'N')
    {
        cout << "turn " << 'E' << endl;
        cout.flush();
    }
    if (me.d == 'E')
    {
        cout << "turn " << 'S' << endl;
        cout.flush();
    }
    if (me.d == 'S')
    {
        cout << "turn " << 'W' << endl;
        cout.flush();
    }
    if (me.d == 'W')
    {
        cout << "turn " << 'N' << endl;
        cout.flush();
    }
}

void turn_l()
{
    if (me.d == 'N')
    {
        cout << "turn " << 'W' << endl;
        cout.flush();
    }
    if (me.d == 'E')
    {
        cout << "turn " << 'N' << endl;
        cout.flush();
    }
    if (me.d == 'S')
    {
        cout << "turn " << 'E' << endl;
        cout.flush();
    }
    if (me.d == 'W')
    {
        cout << "turn " << 'S' << endl;
        cout.flush();
    }
}

void step()
{
    cout << "move" << " " << me.x + dx[ctd[me.d]] << " " << me.y + dy[ctd[me.d]] << endl;
    cout.flush();
}

int dist(pair <int, int> a, pair <int, int> b)
{
    return (b.f - a.f) * (b.f - a.f) + (b.s - a.s) * (b.s - a.s);
}

bool behind(int x1, int y1)
{
    int x0 = me.x, y0 = me.y;
    char sd = me.d;
    if (sd == 'N' && (y1 == y0 + 3) && ((x1 == x0 - 2) || (x1 == x0 - 1) || (x1 == x0) || (x1 == x0 + 1) || (x1 == x0 + 2)))
    {
        return true;
    }
    else if (sd == 'S' && (y1 == y0 - 3) && ((x1 == x0 - 2) || (x1 == x0 - 1) || (x1 == x0) || (x1 == x0 + 1) || (x1 == x0 + 2)))
    {
        return true;
    }
    else if (sd == 'E' && (x1 == x0 + 3) && ((y1 == y0 - 2) || (y1 == y0 - 1) || (y1 == y0) || (y1 == y0 + 1) || (y1 == y0 + 2)))
    {
        return true;
    }
    else if (sd == 'W' && (x1 == x0 - 3) && ((y1 == y0 - 2) || (y1 == y0 - 1) || (y1 == y0) || (y1 == y0 + 1) || (y1 == y0 + 2)))
    {
        return true;
    }
    return false;
}

int main()
{
    for (;;)
    {
        clean();
        read();
        if (finish)
        {
            return 0;
        }
        if (me.f > 0)
        {
            cout << "eat" << " " << me.f << endl;
            cout.flush();
        }
        else if (food.size() == 0)
        {
            turn_r();
            cout.flush();
        }
        else
        {
            bool can_step = true;
            int min_dist;
            for (int i = 0; i < food.size(); ++i)
            {
                if (i == 0 || dist({me.x, me.y}, {food[i].f, food[i].s}) < min_dist)
                {
                    min_dist = dist({me.x, me.y}, {food[i].f, food[i].s});
                    targ_eat = {food[i].f, food[i].s};
                }
            }
            for (int i = 0; i < enemies.size() ; ++i)
            {
                player bad;
                bad = enemies[i];
                if (behind(bad.x, bad.y))
                {
                    cout << "attack" << " " << bad.id << endl;
                    cout.flush();
                    can_step = false;
                    break;
                }
            }
            if (!can_step)
            {
                continue;
            }
            if (me.d == 'N' && me.y == targ_eat.s && me.x <= targ_eat.f) turn_r();
            else if (me.d == 'N' && me.y == targ_eat.s && me.x > targ_eat.f) turn_l();
            else if (me.d == 'E' && me.x == targ_eat.f && me.y < targ_eat.s) turn_l();
            else if (me.d == 'E' && me.x == targ_eat.f && me.y < targ_eat.s) turn_r();
            else if (me.d == 'S' && me.y == targ_eat.s && me.x < targ_eat.f) turn_l();
            else if (me.d == 'S' && me.y == targ_eat.s && me.x < targ_eat.f) turn_r();
            else if (me.d == 'W' && me.x == targ_eat.f && me.y < targ_eat.s) turn_r();
            else if (me.d == 'W' && me.x == targ_eat.f && me.y > targ_eat.s) turn_l();
            else step();
        }
    }
}