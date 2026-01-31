import mediapipe
import cv2
import time
import HandTrackingModule as htm

def getMoves(all_hands):
    right_move = ''
    left_move = ''

    # Process each detected hand
    for hand_data in all_hands:
        land_marks_list, handedness = hand_data
        
        if len(land_marks_list) != 0:
            fingers = []

            # Thumb detection based on handedness
            if handedness == 'Left':  # User's RIGHT hand, which is Left in the model
                if land_marks_list[tips_ids[0]][1] > land_marks_list[tips_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:  # handedness == 'Right' - User's LEFT hand, which is Right in the model
                if land_marks_list[tips_ids[0]][1] < land_marks_list[tips_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            # Other 4 fingers
            for id in range(1, 5):
                if land_marks_list[tips_ids[id]][2] < land_marks_list[tips_ids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            total_fingers = fingers.count(1)

            # Determine the move
            if land_marks_list[8][2] < land_marks_list[6][2] and land_marks_list[12][2] < land_marks_list[10][2] and total_fingers == 2:
                move = 'Scissor'
            elif total_fingers == 0:
                move = 'Rock'
            elif total_fingers == 5:
                move = 'Paper'
            else:
                move = 'choose something'

            # Assign moves correctly
            if handedness == 'Left':
                right_move = move
            else:
                left_move = move
    return right_move, left_move

pTime = 0

wCam, hCam = 1200, 900
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.75)
tips_ids = [4, 8, 12, 16, 20]

# Game state variables
game_state = "waiting"  # waiting, counting, playing
countdown_start = 0
countdown_duration = 3  # 3 seconds countdown

left_wins = 0
right_wins = 0
right_move = ''
left_move = ''


while True:
    key = cv2.waitKey(1) & 0xFF
    success, img = cap.read()

    img = detector.findHands(img)
    all_hands = detector.findPosition(img, draw=False)

    
    if key == ord(' ') and game_state == "waiting":
        game_state = "counting"
        countdown_start = time.time()
        print("Countdown started!")

    # Handle game states
    if game_state == "waiting":
        cv2.putText(img, "Press SPACE to start", (400, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    
    elif game_state == "counting":
        elapsed = time.time() - countdown_start
        remaining = countdown_duration - elapsed
        
        if remaining > 0:
            # Show countdown
            countdown_text = str(int(remaining) + 1)
            cv2.putText(img, countdown_text, (600, 450), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255), 5)
        else:
            # Countdown finished, detect hands
            game_state = "playing"
            print("GO!")
    elif game_state == "playing":
        # get the Right and Left hands moves(rock, paper or scissor)
        right_move, left_move = getMoves(all_hands)
        
        if right_move == 'Rock' and left_move == 'Scissor':
            right_wins += 1
        elif right_move == 'Paper' and left_move == 'Rock':
            right_wins += 1
        elif right_move == 'Scissor' and left_move == 'Paper':
            right_wins += 1
        elif left_move == 'Rock' and right_move == 'Scissor':
            left_wins += 1
        elif left_move == 'Paper' and right_move == 'Rock':
            left_wins += 1
        elif left_move == 'Scissor' and right_move == 'Paper':
            left_wins += 1
        elif right_move == left_move and right_move != '':
            print("It's a tie!")

        # Print results for both hands
        print(f'User Left: {left_move} vs User Right: {right_move}')
        print(f"left: {left_wins}|right: {right_wins}")
        
        # After detecting, go back to waiting state
        game_state = "waiting"
        print("Round finished! Press SPACE to play again")

    cv2.putText(img, f'User Left: {left_move} vs User Right: {right_move}', (225, 70), cv2.FONT_HERSHEY_PLAIN,
                2.5, (255, 0, 0), 3)
    cv2.putText(img, f"left: {left_wins}|right: {right_wins}", (225, 110), cv2.FONT_HERSHEY_PLAIN,
                2.5, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_PLAIN,
                1.5, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if key == ord('q'):
        break