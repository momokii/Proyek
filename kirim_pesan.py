from twilio.rest import Client

twilio_sid = 'AC7df3c60a20e43f481190377c367b9913'
twilio_auth = '9ae6d6a3f0f79d782bce9ebe8424ab30'
twilio_num = '+19853799161'

class Kirim_Pesan:
    def __init__(self, berita):
        self.client = Client(twilio_sid, twilio_auth)
        self.message = self.client.messages.create(
                    body= berita,
                    from_= twilio_num,
                    to= "+6281227041244"
                )
        print(self.message.status)
