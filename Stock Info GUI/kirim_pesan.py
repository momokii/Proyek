from twilio.rest import Client

twilio_sid = 'YOUR_TWILLIO_ID'
twilio_auth = 'YOUR_TWILLIO_AUTH'
twilio_num = '+19853799161'

class Kirim_Pesan:
    def __init__(self, berita):
        self.client = Client(twilio_sid, twilio_auth)
        self.message = self.client.messages.create(
                    body= berita,
                    from_= twilio_num,
                    to= "NUM_DESTINATION"
                )
        print(self.message.status)
