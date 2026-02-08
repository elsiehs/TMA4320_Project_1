#pragma once
#include "widgets/Button.h" 
#include "widgets/TextInput.h" 
#include "AnimationWindow.h"
#include "std_lib_facilities.h"

using namespace TDT4102;

// BEGIN: 5a
constexpr int winW = 0;      // velg vindu bredde
constexpr int winH = 0;      // velg vindu hoyde

constexpr int padX = 0;      // velg x skalering
constexpr int padY = 0;      // velg y skalering
constexpr int radCircle = 0; // velg sirkel radius

// END: 5a

// BEGIN 5
// deklarer playMasterMindVisual her
// END: 5


constexpr int btnW = padX * 2;
constexpr int btnH = padY;      
constexpr Point upperLeftCornerBtn = Point{winW - padX - btnW, padY};

constexpr int inBoxW = winW - 3 * padX - btnW;
constexpr int inBoxH = padY;
constexpr Point upperLeftCornerInBox = Point{padX, padY};

struct Guess {
    const string code; 
    char startLetter = 'a';
};

struct Feedback {
    const int correctPosition = 0;
    const int correctCharacter = 0;
};

// Her defineres klassen MastermindWindow, som arver fra klassen AnimationWindow.
// Det betyr at alle medlemsvariable og medlemsfunksjoner i AnimationWindow, også er en
// del av MastermindWindow. Du kan lese mer om klasser i kapittel 9.4 og om arv
// i kapittel 14.3 i læreboka. Dette skal du lære mer om senere i faget.
class MastermindWindow : public AnimationWindow
{
public:
    MastermindWindow(int x, int y, int w, int h, int size, const std::string &title);

    void cb_guess(){ newGuess(); }

    vector<Guess> guesses;
    vector<Feedback> feedbacks;

    void drawGuessesAndFeedbacks();

    void setCodeHidden(bool hidden);

    string getInput(unsigned int n, char lower, char upper);

private:
    string wait_for_guess();
    void newGuess() { button_pressed = true; }
    void drawCodeHider();
    
    bool button_pressed = false;
    bool code_hidden = true;
    Button guessBtn;
    TextInput guess;
    int size = 0;
};

void addGuess(MastermindWindow &mwin, const string code, const char startLetter);
void addFeedback(MastermindWindow &mwin, const int correctPosition, const int correctCharacter);
