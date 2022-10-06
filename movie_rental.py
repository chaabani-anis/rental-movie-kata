from abc import ABCMeta, abstractmethod


class Render(metaclass=ABCMeta):
    @abstractmethod
    def render_header(self, name):
        pass

    @abstractmethod
    def render_footer(self, frequent_renter_points, total_amount):
        pass

    @abstractmethod
    def render_movie(self, each, this_amount):
        pass


class RenderText(Render):
    def render_header(self, name):
        return "Rental Record for " + name + "\n"

    def render_footer(self, frequent_renter_points, total_amount):
        return "Amount owed is " + str(total_amount) + "\n" \
               + "You earned " + str(frequent_renter_points) + " frequent renter points"

    def render_movie(self, each, this_amount):
        return "\t" + each.getMovie().getTitle() + "\t" + str(this_amount) + "\n"

class Customer:


    def __init__(self, name):
        self._rentals = []
        self.name = name

    def getName(self):
        return self.name

    def statement(self, render: Render):
        total_amount = 0
        frequent_renter_points = 0
        result = render.render_header(self.getName())

        for rental in self._rentals:
            this_amount = 0.0
            this_amount = rental.determine_amounts()
            result += render.render_movie(rental, this_amount)
            total_amount += this_amount

        frequent_renter_points = self.compute_renter_points()

        result += render.render_footer(frequent_renter_points, total_amount)

        return result

    def addRental(self, param):
        self._rentals.append(param)

    def compute_renter_points(self):
        return sum(map(lambda rental: rental.add_frequent_renter_points(), self._rentals))


class Movie:
    CHILDRENS = 2
    NEW_RELEASE = 1
    REGULAR = 0

    def __init__(self, title, priceCode):
        self.title = title
        self.priceCode = priceCode

    def getPriceCode(self):
        return self.priceCode

    def setPriceCode(self, arg):
        self.priceCode = arg

    def getTitle(self):
        return self.title


class Rental:
    def __init__(self, movie, daysRented):
        self.daysRented = daysRented
        self.movie = movie

    def getDaysRented(self):
        return self.daysRented

    def getMovie(self):
        return self.movie

    def add_frequent_renter_points(self):
        frequentRenterPoints = 1
        # add bonus for a two day new release rental
        if (self.getMovie().getPriceCode() == Movie.NEW_RELEASE) and self.getDaysRented() > 1:
            frequentRenterPoints += 1
        return frequentRenterPoints

    def determine_amounts(self):
        thisAmount = 0.0
        if self.getMovie().getPriceCode() == Movie.REGULAR:
            thisAmount += 2
            if self.getDaysRented() > 2:
                thisAmount += (self.getDaysRented() - 2) * 1.5
        elif self.getMovie().getPriceCode() == Movie.NEW_RELEASE:
            thisAmount += self.getDaysRented() * 3
        elif self.getMovie().getPriceCode() == Movie.CHILDRENS:
            thisAmount += 1.5
            if self.getDaysRented() > 3:
                thisAmount += (self.getDaysRented() - 3) * 1.5
        return thisAmount
