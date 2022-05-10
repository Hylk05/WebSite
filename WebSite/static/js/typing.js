let print = console.log;

let xhr = new XMLHttpRequest();
xhr.open('POST', document.location.href + '/done', false);


const text = document.querySelector('.typing_text');
let currentWord = text.firstElementChild;
let currentLetter = currentWord.firstElementChild;
let currentLetterCoords = currentLetter.getBoundingClientRect();
const cursor = document.querySelector('.cursor');

let speedCounter = document.querySelector('.speed_counter');
let errorsCounter = document.querySelector('.errors_counter');
let lettersCounter = 0;

// Всё, что касается времени
const timer = document.querySelector('.timer');
let time = Date; // для контроля времени
const startTime = time.now();
function update_timer(timer)
{
    let seconds = Number(timer.textContent.slice(2, 4));
    let minutes = Number(timer.textContent.slice(0, 1));
    if (seconds < 59){
        seconds = String(++seconds)
        seconds.length == 1 ? seconds = '0' + seconds : seconds = seconds
        minutes = String(minutes)}
    else{
        minutes++
        seconds = String('00')};

    if (lettersCounter) {speedCounter.textContent = String(Math.ceil(lettersCounter / (Number(minutes) + Number(seconds) / 60)))};
    timer.textContent = minutes + ':' + seconds;
};
setInterval(update_timer, 1000, timer);

// Обработчик нажатия на клавишу
function type(event)
{
    // Обработка нажатия, сдвиг буквы или слова, если буква в нём последняя
    if (event.key === currentLetter.textContent)
    {
        currentLetter.classList.add("typed_letter")
        lettersCounter++
        if (currentLetter.nextElementSibling)
        {
            currentLetter = currentLetter.nextElementSibling
        }
        else if (currentWord.nextElementSibling)
        {
            currentWord = currentWord.nextElementSibling
            currentLetter = currentWord.firstElementChild
        }
        else // Если дальше слов нет, урок завершён
        {    // Ниже - всё, что происходит при завершении урока
            cursor.style.top = '-10px;';

            //let response = fetch(document.location.href + '/done')
            xhr.send(timer.textContent + ';' + String(lettersCounter))
            window.location.href = document.location.href + '/info'
        };
    }
    else if (!event.repeat)
    {
        errorsCounter.textContent = Number(errorsCounter.textContent) + 1
    };

      // Сдвиг курсора

    if (currentLetter.textContent == ' ')
    { // Если сейчас пробел, то высота не обновляется, потому что пробел имеет нулевую высоту
    currentLetterCoords.x = currentLetter.getBoundingClientRect().x;
    }
    else
    {
    currentLetterCoords = currentLetter.getBoundingClientRect();
    };

    cursor.style.left = String(Math.floor(currentLetterCoords.x)) + 'px';
    cursor.style.top = String(currentLetterCoords.y + 10) + 'px';
};

document.addEventListener('keydown', type);
