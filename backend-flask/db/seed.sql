-- manually created

INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
    ('Oliver Bebber', 'oliverbebber' ,'MOCK'), --- hard coding, need to come back to redo
    ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
    (
        (SELECT uuid from public.users WHERE users.handle = 'oliverbebber' LIMIT 1), -- hard coding, need to come back to redo
        'This was imported as seed data!',
        current_timestamp + interval '10 day'
    )