# /// script
# dependencies = [
# "pygame-ce",
# "cffi",
# "pymunk",
# "math",
# ]
# ///

from levels import *
import asyncio

current_level, space = (setup_level1((0, 0)))
running = True



async def main():
    global screen, space, screen_blur, current_level, running, clock, logo_img, play_img, first_screen_img

    play_rect = play_img.get_rect()
    play_rect.topleft = 512 - play_img.get_width() / 2, 500
    menu_lighting = light_group_setup([((512, 384), 500)])
    transition = False
    menu = True
    push_group, time_freeze, last_keys, level_start_time, event_finished, movement, allow_freeze, starting_pos = reset_level(current_level)
    while running:
        if menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False, pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_rect.collidepoint(pygame.mouse.get_pos()):
                        transition = True
            screen.fill("#7b7b7b")
            screen.blit(logo_img, (512 - logo_img.get_width() / 2, 100))
            screen.blit(play_img, (512 - play_img.get_width() / 2, 500))
            screen_lighting(menu_lighting, screen)
            if transition:
                first_screen_img.set_alpha(first_screen_img.get_alpha() + 10)
                screen.blit(first_screen_img, (0,0))
                if first_screen_img.get_alpha() >= 255:
                    menu = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            screen.blit(background_imgs[current_level[5]], (0, 0))
            screen.blit(screen_blur, (0, 0))

            if current_level[5] > 5:
                if event.type == pygame.MOUSEBUTTONUP:
                    if allow_freeze:
                        if not time_freeze:
                            push_group.append(circle_push(pygame.mouse.get_pos(), space))
                    else:
                        push_group.append(circle_push(pygame.mouse.get_pos(), space))
            if movement:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and not last_keys[pygame.K_w]:
                    if not current_level[2].jump(current_level[0]):
                        current_level[2].jump(current_level[1])
                if keys[pygame.K_SPACE] and not last_keys[pygame.K_SPACE] and allow_freeze:
                    time_freeze = not time_freeze
                    for item in current_level[0]:
                        item.change_type()
                    current_level[2].change_type()
                if keys[pygame.K_r] and not last_keys[pygame.K_r]:
                    current_level[5] -= 1
                    current_level, space = setup_next_level(starting_pos, current_level)
                    push_group, time_freeze, last_keys, level_start_time, event_finished, movement, allow_freeze, starting_pos = reset_level(current_level)
                last_keys = keys

            for pygame_item in current_level[4]:
                if pygame_item.update(screen, current_level[2]):
                    if pygame_item.type == "kill":
                        current_level[5] -= 1
                        current_level, space = setup_next_level(starting_pos, current_level)
                        push_group, time_freeze, last_keys, level_start_time, event_finished, movement, allow_freeze, starting_pos = reset_level(current_level)
                if pygame_item.update(screen, current_level[2]):
                    if pygame_item.type == "win":
                        current_level, space = setup_next_level(current_level[2].rect.center, current_level)
                        push_group, time_freeze, last_keys, level_start_time, event_finished, movement, allow_freeze, starting_pos = reset_level(current_level)

            for circle in push_group:
                if not circle.alive:
                    push_group.remove(circle)
                circle.update(space, screen)

            for static_item in current_level[1]: static_item.update(screen, space)
            for phys_item in current_level[0]: phys_item.update(screen, space)
            screen_blur.blit(screen.convert(), (0, 0))

            current_level[2].update(screen, space, movement)

            # Level specific events
            if current_level[5] == 0 and not event_finished:
                if pygame.time.get_ticks() - level_start_time >= 2000:
                    space.remove(current_level[1][2].body, current_level[1][2].rotation_limit_body,
                                 current_level[1][2].poly)
                    current_level[1].pop(2)
                    event_finished = True

            current_level[3][0][0] = current_level[2].rect.center
            screen_lighting([*current_level[3]], screen)

            pygame.display.flip()
        clock.tick(fps)
        for x in range(7):
            space.step(0.002)
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())