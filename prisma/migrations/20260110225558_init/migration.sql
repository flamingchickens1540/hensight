-- CreateTable
CREATE TABLE "Event" (
    "key" TEXT NOT NULL,
    "pointsScored" INTEGER,
    "averagePointsPerMatch" INTEGER,
    "rpEarned" INTEGER,
    "penaltyPoints" INTEGER,
    "autoPoints" INTEGER,
    "matchesPlayed" INTEGER,
    "feetClimbed" INTEGER,

    CONSTRAINT "Event_pkey" PRIMARY KEY ("key")
);

-- CreateIndex
CREATE UNIQUE INDEX "Event_key_key" ON "Event"("key");
