import pandas as pd

df=pd.read_csv("hotels.csv", dtype={"id":str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cardsecurity=pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id=hotel_id
        self.name=df.loc[df["id"]==self.hotel_id, "name"].squeeze()
       

    def book_hotel(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"]==self.hotel_id, "available"]= "no"
        df.to_csv("hotels.csv", index=False)
        

    def available(self):
        """Check if the hotel is available"""
        availability=df.loc[df["id"]==self.hotel_id, "available"].squeeze()
        if availability =="yes":
            return True
        else:
            return False

class SpaHotel(Hotel):
    def book_spa_package(self):
        pass

class ReservationConfermation:
    def __init__(self, customer_name, hotel_obj):
        self.customer_name=customer_name
        self.hotel=hotel_obj

    def generate(self):
        content=f"""
        Thank you for your reservation
        Here is your booking data:
        Name:{self.customer_name}
        Hotel name:{self.hotel.name}
        """
        return content
    
class CreditCard:
    def __init__(self, number):
        self.number=number
   
    
    def validate(self, expiration, holder, cvc):
        for card in df_cards:
            if (card["number"] == self.number and
                card["expiration"] == expiration and
                card["holder"] == holder and
                card["cvc"] == cvc):
                return True
        return False

class CreditcardSecurity(CreditCard):
    def security(self, given_password):
        password=df_cardsecurity.loc[df_cardsecurity["number"]==self.number, "password"].squeeze()
        if password==given_password:
            return True
        else:
            return False


class SpapackageReservtion:
     def __init__(self, customer_name, hotel_obj):
        self.customer_name=customer_name
        self.hotel=hotel_obj
     
     def generate(self):
        content=f"""
        Thank you for your SPA reservation
        Here is your SPA booking data:
        Name:{self.customer_name}
        Hotel name:{self.hotel.name}
        """
        return content


print(df)

hotel_ID=input("Enter the id of the hotel:")
hotel=SpaHotel(hotel_ID)

if hotel.available():
    credit_card=CreditcardSecurity(number="1234")
    if credit_card.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
        if credit_card.security(given_password="mypass"):
            hotel.book_hotel()
            name=input("Enter a name:")
            reservation_confermation=ReservationConfermation(customer_name=name, hotel_obj=hotel)
            print(reservation_confermation.generate())
            spa=input("Do you want want to book a spa package?")
            if spa== "yes":
                hotel.book_spa_package()
                reservtion_Spapackage=SpapackageReservtion(customer_name=name, hotel_obj=hotel)
                print(reservtion_Spapackage.generate())
        else:
            print("Information is not correct")
    else:
        print("There was a problem with your payment")

else:
    print("Hotel is not free")