self.x += self.x_vector
        self.y += self.y_vector
        if self.x <= 0 or self.x >= W-64:
            self.x_vector = -self.x_vector  # Reversing Horizontal direction for boundaries
    
        if self.y >= beltY and not self.crossed:
            global score, health
            score -= 1
            health -= HEALTH_DECREASE_CROSS #Reduce health when enemy crosses
            if health < 0:
                health = 0
            self.crossed = True
            # print(score)